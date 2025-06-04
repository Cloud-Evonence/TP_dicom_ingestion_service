Project Overview:
This project implements an automated pipeline to extract, process, and store DICOM metadata and image previews using GCP-native services. It is designed to support diagnostic imaging use cases by generating image snapshots and structured metadata from .dcm files, storing results in GCS and BigQuery for further analysis.


Architecture Components:
GCS (Google Cloud Storage): Stores input DICOM files and output artifacts (images and JSON metadata).
Cloud Functions (Gen 2): Stateless serverless compute that processes .dcm files and triggers on file uploads to GCS.
BigQuery: Stores extracted metadata from DICOM files in a structured table for querying and analytics.
Cloud Build: CI/CD pipeline that deploys the Cloud Function automatically on commits to the main GitHub branch.
GitHub: Version control system to manage source code and pipeline configurations.
VPC Connector: Enables secure network communication between the Cloud Function and other GCP services.

DICOM Files & Attributes:
Input Format: .dcm files
Metadata Extracted: Patient ID, Study Date, Modality, Pixel Spacing, Image Dimensions, etc.
Image Output:  .png preview generated from each .dcm file

GCS Buckets:
Input Bucket: tp_dicom
Folder: INPUT_FOLDER/
Output Buckets (same bucket):
Images: tp_dicom/OUTPUT_IMAGE_FOLDER/images/*.png
Metadata: tp_dicom/OUTPUT_JSON_FOLDER/metadata/*.json
GCS Security:
Bucket-level permissions should be restricted using IAM roles (e.g., roles/storage.objectViewer for readers).
Enforce uniform bucket-level access.
Enable object versioning if needed.

Cloud Function [ Gen2 ]:
Name: process_dicom_file
Runtime: Python 3.10
Trigger: Finalize event on GCS (google.storage.object.finalize)
Region: us-central1
Entry Point: process_dicom_file
Source: GitHub repo root directory
Memory: 512MB
Timeout: 300s

Repository Structure:

TP_dicom_ingestion_service/
├── .cloudbuild/
│   └── cloudbuild.yaml
├── config.py
├── extractor.py
├── main.py
├── requirements.txt
└── README.md


Deployment Steps Via Cloud Build:
1. Clone Repo & Create Branch
git clone https://github.com/your-org/TP_dicom_ingestion_service.git
cd TP_dicom_ingestion_service
git checkout -b cicd-pipeline
	
2. Create cloudbuild.yaml in .cloudbuild/

steps:
  - name: 'gcr.io/cloud-builders/gcloud'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        echo "Deploying DICOM processing Cloud Function..."

        gcloud functions deploy process_dicom_file \
          --gen2 \
          --runtime python310 \
          --entry-point process_dicom_file \
          --trigger-bucket tp_dicom \
          --trigger-event google.storage.object.finalize \
          --source=. \
          --region us-central1 \
          --memory 512MB \
          --timeout 300s \
          --vpc-connector your-vpc-connector-name \
          --set-env-vars CONFIG_ENV=prod \
          --quiet
options:
  logging: CLOUD_LOGGING_ONLY
3. Connect GitHub Repo to Cloud Build
Go to Cloud Build > Triggers
Create trigger:
Source: GitHub repository
Branch: main
Directory: . (or wherever the function source lives)
Build config file: .cloudbuild/cloudbuild.yaml
4. Push Code to GitHub
git add .
git commit -m "Implement Cloud Function CI/CD pipeline"
git push origin cicd-pipeline
5. Open Pull Request
Use GitHub UI to open a PR from cicd-pipeline to main. After merging, Cloud Build will trigger and deploy the function.
