#import the standard necessary libraries
import os
import uuid
import mimetypes
from pathlib import Path
from datetime import datetime, timezone

# FastAPI imports for request handling and dependency injection
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

# Local application imports
from . import models, schemas
from .database import get_db

# Directory where uploaded files will be stored locally
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

# Allowed MIME types
ALLOWED_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "text/plain",
    "application/octet-stream",
}

# Create a router to group API endpoints together
router = APIRouter()

# Ensure uploads dir exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#Endpoint: Upload a file to the server.
@router.post("/upload", response_model=schemas.FileMetadata)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
# Step 1: Read file content into memory and check size
    contents = await file.read()
    size = len(contents)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (>20MB)")

# Step 2: Validate MIME type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

# Step 3: Create a unique ID and safe disk filename
    file_id = str(uuid.uuid4())
    disk_name = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, disk_name)
 # Step 4: Save file to disk
    with open(file_path, "wb") as f:
        f.write(contents)

# Step 5: Create and save metadata in the database
    meta = models.File(
        file_id=file_id,
        file_name=file.filename,       #original name   
        size=size,
        upload_timestamp=datetime.now(timezone.utc),
    )
    db.add(meta)
    db.commit()
    db.refresh(meta) # refresh instance to get updated fields like auto-ID
    return meta



#Endpoint: List all uploaded files sorted by upload date (newest first). Fetches metadata from the database only — no file content.
@router.get("/files", response_model=list[schemas.FileMetadata])
def list_files(db: Session = Depends(get_db)):
    return db.query(models.File).order_by(models.File.upload_timestamp.desc()).all()

# Endpoint: Download a file by its unique file ID.
@router.get(
    "/files/{file_id}",
    summary="Download File",
    responses={200: {"content": {"application/octet-stream": {}}}},
)
def download_file(file_id: str, db: Session = Depends(get_db)):
# Step 1: Check if file exists in database
    meta = db.query(models.File).filter(models.File.file_id == file_id).first()
    if not meta:
        raise HTTPException(status_code=404, detail="File not found in DB")

# Step 2: Look for the file in the uploads directory
    for name in os.listdir(UPLOAD_FOLDER):
        if name.startswith(file_id + "_"):
            path = Path(UPLOAD_FOLDER) / name
            if not path.exists():
                break
# Step 3: Determine MIME type for correct Content-Type
            media_type, _ = mimetypes.guess_type(str(path))
            return FileResponse(
                path,
                media_type=media_type or "application/octet-stream",
                filename=meta.file_name,  # forces "attachment" with original filename
            )
# Step 4: If not found on disk, return 404
    raise HTTPException(status_code=404, detail="File missing on disk")
