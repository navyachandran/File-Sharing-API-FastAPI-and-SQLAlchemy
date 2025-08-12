#import the necessary libraries
from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from datetime import datetime

"""
Schema: File metadata model for API responses.
This schema is used to define the structure of the file information
returned by the API when a file is uploaded, listed, or downloaded. 
"""
class FileMetadata(BaseModel):
    file_id: str #A unique identifier (UUID) for the file.
    file_name: str  # The original name of the uploaded file.
    size: int #The file size in bytes.
    upload_timestamp: datetime #The date and time (UTC) when the file was uploaded.

# Configures Pydantic to allow initialization from ORM objects
    model_config = ConfigDict(from_attributes=True)
