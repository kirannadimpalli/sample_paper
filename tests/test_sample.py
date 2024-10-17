from fastapi.testclient import TestClient
from sample_paper.app import app
import mongomock
from sample_paper.config import db

def mock_db():
    return mongomock.MongoClient().db_name

app.dependency_overrides[db] = mock_db


client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "welcome to ZuAI"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_paper():
    response = client.post("/papers", json={"title": "Test Paper", "content": "This is a test."})
    assert response.status_code == 200


def test_get_paper():
    sample_paper = {
        "title": "Sample Paper Title",
        "author": "John Doe",
        "content": "This is the content of the paper."
    }
    create_response = client.post("/papers", json=sample_paper)
    paper_id = create_response.json()["paper_id"]

    response = client.get(f"/papers/{paper_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Paper Title"

def test_update_paper():
    sample_paper = {
        "title": "Sample Paper Title",
        "author": "John Doe",
        "content": "This is the content of the paper."
    }
    create_response = client.post("/papers", json=sample_paper)
    paper_id = create_response.json()["paper_id"]

    update_data = {"content": "Updated content"}
    response = client.put(f"/papers/{paper_id}", json=update_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Paper updated successfully"}

def test_delete_paper():
    sample_paper = {
        "title": "Sample Paper Title",
        "author": "John Doe",
        "content": "This is the content of the paper."
    }
    create_response = client.post("/papers", json=sample_paper)
    paper_id = create_response.json()["paper_id"]

    response = client.delete(f"/papers/{paper_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Paper deleted successfully"}


def test_extract_pdf():
    pdf_bytes = b"%PDF-1.4 sample content"
    files = {"file": ("test.pdf", pdf_bytes, "application/pdf")}
    response = client.post("/extract/pdf", files=files)
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert response.json()["status"] == "pending"


def test_get_task_status():
    task_id = "sample_task_id"
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404 or response.status_code == 200
    if response.status_code == 200:
        assert "task_id" in response.json()


def test_extract_text():
    text_input = {
        "text": "This is some sample text from a document."
    }
    response = client.post("/extract/text", json=text_input)
    assert response.status_code == 200
    assert "title" in response.json()
    assert "author" in response.json()
