#Import necessary libraries
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from .database import Base

# ORM model representing the 'files' table in the database
class File(Base):
    __tablename__ = "files"#name of the table 

    id = Column(Integer, primary_key=True, index=True)# Primary key ID  — unique identifier in the DB
    file_id = Column(String, unique=True, index=True) # Unique file identifier used internally for downloads
    file_name = Column(String)# Original file name as uploaded by the user
    size = Column(Integer)# File size in bytes
    upload_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc)) # Timestamp of when the file was uploaded, defaults to the current UTC time
