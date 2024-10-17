from .config import  db
import base64
from .utils import extract_pdf_data, extract_pdf_content
import asyncio

from celery import Celery

celery_app = Celery(
    "sample_paper",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

celery_app.autodiscover_tasks(['sample_paper'])



from io import BytesIO
from .config import db
import base64

@celery_app.task
def process_pdf_task(task_id, pdf_content_base64):
    """Celery task to process the PDF content asynchronously."""
    
    # Decode the base64 encoded PDF content back to binary
    pdf_content = base64.b64decode(pdf_content_base64)

    # Wrap pdf_content in BytesIO to simulate a file-like object
    pdf_stream = BytesIO(pdf_content)

    # Simulate PDF text extraction
    pdf_text = extract_pdf_content(pdf_stream)

    # Use asyncio to run async operations synchronously
    loop = asyncio.get_event_loop()
    paper_id = loop.run_until_complete(process_and_save_pdf_data(task_id, pdf_text))
    return paper_id


# Async function to handle processing and saving of data
async def process_and_save_pdf_data(task_id, pdf_text):
    # Simulate extracting sample paper data
    sample_paper_json = extract_pdf_data(pdf_text)

    # Save the extracted paper data into the database asynchronously
    paper_id = await save_extract_data(sample_paper_json)

    # Update the task status to 'completed' and save the paper_id asynchronously
    result = await update_status(task_id, paper_id)

    # Check if the update was successful
    if result.matched_count == 0:
        print("Task status not updated")
    else:
        print("Task status updated")
    
    return paper_id


# Async function to save extracted data
async def save_extract_data(sample_paper_json):
    result = await db.papers.insert_one(sample_paper_json)  # Assume db.papers is your MongoDB collection
    return str(result.inserted_id)

# Async function to update task status
async def update_status(task_id, paper_id):
    result = await db.tasks.update_one(
        {"task_id": task_id},
        {"$set": {"status": "completed", "paper_id": paper_id}}
    )
    return result