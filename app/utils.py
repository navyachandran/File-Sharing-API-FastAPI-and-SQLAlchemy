#import the necessary libraries
import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from typing import Tuple

#Directory where uploaded files will be stored
UPLOAD_FOLDER = "uploads"

# Ensure uploads directory exists before saving the files
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)


#Saves an uploaded file to disk and returns its metadata.
def save_file(file: UploadFile) -> Tuple[str, str, int, str]:
    file_id = str(uuid.uuid4())
    file_name = file.filename
    extension = Path(file_name).suffix  # Currently unused, but could be used for validation
    saved_path = Path(UPLOAD_FOLDER) / f"{file_id}_{file_name}" #The absolute or relative path where the file was saved.

#Save the file to disk
    with open(saved_path, "wb") as f:
        contents = file.file.read()
        f.write(contents)
#Return metadata
    return file_id, file_name, len(contents), str(saved_path)
