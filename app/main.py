#This file acts as the entry point for the FastAPI Application


#import all the necessary libraries
from fastapi import FastAPI
from . import models
from .database import engine
from .routes import router

#Create all database tables defined in models.py
#If the tables exists already then SQLAchemy skips the creation 
models.Base.metadata.create_all(bind=engine)

# Declaring FastAPI application with a title and description
app = FastAPI(title=" File Sharing API", description="Simple API for uploading, listing, and downloading files")

#this includes all the endpoints from routes.py
app.include_router(router)


#This health check  endpoint is used to verify if the API is running 
@app.get("/health")
def health():
    return {"status": "ok"}
