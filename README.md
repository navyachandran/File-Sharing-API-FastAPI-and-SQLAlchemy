# File Sharing API – FastAPI + SQLAlchemy
A simple File Sharing API built with FastAPI and SQLAlchemy that used Local - Disk Storage.
It supports:

1) Uploading files (up to 20 MB, with type validation)
2) Listing uploaded files
3) Downloading files by ID
4) All data is stored locally in a SQLite database and the uploaded files are saved on disk.


# 1.Prerequisites
Python 3.10+
git, pip
macOS/Linux terminal or Windows PowerShell

# 2.Get the code and set up a virtual environment
### a)Clone the repo:

git clone <repo_url>

### b)create and activate venv:

python3 -m venv venv

### c)macOS/Linux:

source venv/bin/activate

 # 3.Install dependencies mentioned in requirements.txt

:
➡ pip install -r requirements.txt

# 4. To run the code 

### a)default port 8000:

#### uvicorn app.main:app --reload

#### (or) to choose a clean port :

uvicorn app.main:app --reload --port 9000

### c)Once running, open Swagger UI and test all the endpoints by uploading,listing and downloading files:
#### http://127.0.0.1:8000/docs (or 9000 if you used a custom port)

# API ENDPOINTS
| Method | Endpoint           | Description             |
| ------ | ------------------ | ----------------------- |
| POST   | `/upload`          | Upload a file           |
| GET    | `/files`           | List all uploaded files |
| GET    | `/files/{file_id}` | Download file by ID     |
| GET    | `/health`          | API health check        |


# 5.To run the test case :

#### pytest -q

# 6.Reset local state (clean slate):
### remove uploaded files and database

#### rm -rf app/uploads/*


#### rm -f app/files.db

