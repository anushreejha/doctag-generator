import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_status():
    """Test the /status/ endpoint."""
    response = client.get("/status/")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}

def test_generate_tags_valid():
    """Test the /generate-tags/ endpoint with a valid text file."""
    file_content = "Deep learning techniques are widely used in AI research."
    files = {"file": ("test.txt", file_content, "text/plain")}
    
    response = client.post("/generate-tags/", files=files)
    
    assert response.status_code == 200
    assert "tags" in response.json()
    assert isinstance(response.json()["tags"], list)  # Ensure it's a list

def test_generate_tags_empty_file():
    """Test /generate-tags/ with an empty file."""
    files = {"file": ("empty.txt", "", "text/plain")}
    
    response = client.post("/generate-tags/", files=files)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty."

def test_generate_tags_failure():
    """Test /generate-tags/ when the model fails to generate tags."""
    # Simulating an invalid input that could cause failure
    file_content = " "  # Just a space, should ideally return no tags
    files = {"file": ("test.txt", file_content, "text/plain")}

    response = client.post("/generate-tags/", files=files)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Failed to generate tags."

