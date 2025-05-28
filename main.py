import tempfile
import json
import pydicom
from google.cloud import storage, bigquery
from config import CONFIG
from extractor import extract_metadata, save_image

def process_dicom_file(event, context):
    file_name = event['name']
    bucket_name = event['bucket']

    if not file_name.endswith(".dcm"):
        print(f"Skipping non-DICOM file: {file_name}")
        return

    if not file_name.startswith("INPUT_FOLDER/"):
        print(f"Skipping file not in INPUT_FOLDER: {file_name}")
        return

    print(f"Processing file: {file_name} from bucket: {bucket_name}")

    storage_client = storage.Client()
    bq_client = bigquery.Client()

    # Step 1: Download DICOM file
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    with tempfile.NamedTemporaryFile(suffix=".dcm") as tmp_file:
        blob.download_to_filename(tmp_file.name)
        ds = pydicom.dcmread(tmp_file.name, force=True)

        # Step 2: Extract metadata
        metadata = extract_metadata(ds, file_name)

        # Step 3: Save image to GCS
        image = save_image(ds)
        image_filename = file_name.split("/")[-1].replace(".dcm", ".png")  # Just the filename
        with tempfile.NamedTemporaryFile(suffix=".png") as img_tmp:
            image.save(img_tmp.name)
            image_blob_path = f"{CONFIG['output_image_prefix']}{image_filename}"
            image_blob = bucket.blob(image_blob_path)
            image_blob.upload_from_filename(img_tmp.name)
            print(f"Uploaded image to GCS: {image_blob.name}")

        image_url = f"https://storage.cloud.google.com/{bucket_name}/{image_blob_path}"
        # Add image_url to metadata before uploading JSON and inserting into BQ
        metadata["image_url"] = image_url

        # Step 4: Save metadata JSON to GCS
        metadata_filename = file_name.split("/")[-1].replace(".dcm", ".json")
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json") as json_tmp:
            json.dump(metadata, json_tmp, indent=2)
            json_tmp.flush()
            metadata_blob_path = f"{CONFIG['output_metadata_prefix']}{metadata_filename}"
            metadata_blob = bucket.blob(metadata_blob_path)
            metadata_blob.upload_from_filename(json_tmp.name)
            print(f"Uploaded metadata to GCS: {metadata_blob.name}")

        # Step 5: Insert into BigQuery
        table_ref = bq_client.dataset(CONFIG["bq_dataset"]).table(CONFIG["bq_table"])
        errors = bq_client.insert_rows_json(table_ref, [metadata])
        if errors:
            raise RuntimeError(f"BigQuery insert errors: {errors}")
        print(f"Inserted metadata to BigQuery table: {CONFIG['bq_table']}")