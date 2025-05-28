import pydicom
from PIL import Image
import numpy as np
from iod_schema_map import IOD_FIELD_MAP

def get_fields_for_sop_uid(sop_uid):
    return IOD_FIELD_MAP.get(str(sop_uid), IOD_FIELD_MAP["default"])

def extract_metadata(ds, filename):
    sop_uid = ds.get("SOPClassUID", "default")
    iod_info = get_fields_for_sop_uid(sop_uid)
    metadata = {
        "IODType": iod_info["iod_type"],
        "SOPClassUID": str(sop_uid),
        "SourceFile": filename
    }
    for field in iod_info["fields"]:
        try:
            value = ds.get(field, None)
            if value is not None:
                if isinstance(value, (list, pydicom.multival.MultiValue)):
                    value = [str(v) for v in value]
                else:
                    value = str(value)
            metadata[field] = value
        except Exception as e:
            metadata[field] = f"Error: {e}"
    return metadata

def save_image(ds):
    arr = ds.pixel_array
    arr = (arr - arr.min()) / (np.ptp(arr) + 1e-5) * 255
    img = Image.fromarray(arr.astype(np.uint8))
    if img.mode != "L":
        img = img.convert("L")
    return img