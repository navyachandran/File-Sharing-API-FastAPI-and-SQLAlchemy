from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path

# Create a test client for our FastAPI app
client = TestClient(app)

#Test: Upload a file that is exactly 20MB.
#Should be accepted (HTTP 200) and stored with the correct size.
def test_limit_accept_20mb(tmp_path: Path):

     # Create a dummy file filled with null bytes of size exactly 20MB
    p = tmp_path / "ok.bin"
    p.write_bytes(b"\0" * (20 * 1024 * 1024))  # exactly 20MB
    # Open the file and send it to the API
    with p.open("rb") as f:
        r = client.post("/upload", files={"file": ("ok.bin", f, "application/octet-stream")})
    # Verify the API accepted the file
    assert r.status_code == 200
    assert r.json()["size"] == 20 * 1024 * 1024 # Check stored size


#Upload a file that is larger than 20MB (20MB + 1 byte).
#Should be rejected with HTTP 413 (Payload Too Large).
def test_limit_reject_over_20mb(tmp_path: Path):
    # Create a dummy file slightly over the limit
    p = tmp_path / "big.bin"
    p.write_bytes(b"\0" * (20 * 1024 * 1024 + 1))  # 20MB + 1
    # Try uploading
    with p.open("rb") as f:
        r = client.post("/upload", files={"file": ("big.bin", f, "application/octet-stream")})
    # Verify rejection
    assert r.status_code == 413

#Upload a file with a non-ASCII filename
def test_non_ascii_filename(tmp_path: Path):
     # Create a small text file with a non-ASCII name
    p = tmp_path / "resumé.txt"
    p.write_text("hello")
     # Upload the file
    with p.open("rb") as f:
        r = client.post("/upload", files={"file": ("résumé.txt", f, "text/plain")})
    assert r.status_code == 200
    # Extract file_id from response
    fid = r.json()["file_id"]
    # Download the file using its file_id
    r = client.get(f"/files/{fid}")
    assert r.status_code == 200
    # Verify the "Content-Disposition" header is set correctly for attachment
    assert "attachment;" in r.headers.get("content-disposition", "").lower()
