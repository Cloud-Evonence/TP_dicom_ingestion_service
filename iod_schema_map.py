IOD_FIELD_MAP = {
    "1.2.840.10008.5.1.4.1.1.2": {
        "iod_type": "CTImage",
        "fields": [
            "PatientName" , "PatientID" , "PatientBirthDate" , "PatientSex" , "PatientIdentityRemoved" , "DeidentificationMethod" , "DeidentificationMethodCodeSequence" ,
            "StudyInstanceUID" , "StudyDate" , "StudyTime" , "ReferringPhysicianName" , "StudyID" , "AccessionNumber" , "StudyDescription" , "PatientAge" , "PatientWeight" ,
            "Modality" , "SeriesInstanceUID" , "SeriesNumber" , "SeriesDate" , "SeriesTime" , "ProtocolName" , "SeriesDescription" , "BodyPartExamined" , "PatientPosition" ,
            "SmallestImagePixelValue" , "LargestImagePixelValue" , "ImageOrientationPatient" , "FrameOfReferenceUID" , "PositionReferenceIndicator" , "Manufacturer" , "StationName" ,
            "ManufacturerModelName" , "DeviceSerialNumber" , "SoftwareVersions" , "GantryDetectorTilt" , "DateOfLastCalibration" , "TimeOfLastCalibration" , "PixelPaddingValue" ,
            "PixelSpacing" , "ImagePositionPatient" , "SliceThickness" , "SliceLocation" , "ImageType" , "SamplesPerPixel" , "PhotometricInterpretation" , "BitsAllocated" ,
            "BitsStored" , "HighBit" , "RescaleIntercept" , "RescaleSlope" , "KVP" , "AcquisitionNumber" , "ScanOptions" , "DataCollectionDiameter" , "ReconstructionDiameter" ,
            "DistanceSourceToDetector" , "DistanceSourceToPatient" , "TableHeight" , "RotationDirection" , "ExposureTime" , "XRayTubeCurrent" , "Exposure" , "FilterType" ,
            "GeneratorPower" , "FocalSpots" , "ConvolutionKernel" , "SOPClassUID" , "SOPInstanceUID" , "SpecificCharacterSet" , "InstanceCreationDate" , "InstanceCreationTime" ,
            "InstanceNumber", "image_url"
        ]
    },
    "1.2.840.10008.5.1.4.1.1.4": {
        "iod_type": "MRImage",
        "fields": [
            "PatientID", "StudyDate", "Modality", "EchoTime", "RepetitionTime",
            "Rows", "Columns", "StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID",
            "image_url"
        ]
    },
    "default": {
        "iod_type": "Generic",
        "fields": ["PatientID", "Modality", "SOPInstanceUID",
        "image_url"]
    }
}