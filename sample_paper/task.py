import base64
import asyncio
from io import BytesIO
from celery import Celery

from .config import  db
from .utils import extract_pdf_data, extract_pdf_content
from .entity import SamplePaper


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


@celery_app.task
def process_pdf_task(task_id, pdf_content_base64):
    """Celery task to process the PDF content asynchronously."""
    
    pdf_content = base64.b64decode(pdf_content_base64)
    pdf_stream = BytesIO(pdf_content)
    pdf_text = extract_pdf_content(pdf_stream)

    loop = asyncio.get_event_loop()
    paper_id = loop.run_until_complete(process_and_save_pdf_data(task_id, pdf_text))
    return paper_id


async def process_and_save_pdf_data(task_id, pdf_text):
    sample_paper_json = extract_pdf_data(pdf_text)
    paper = SamplePaper(**sample_paper_json)

    paper_id = await save_extract_data(paper.dict())
    result = await update_status(task_id, paper_id)

    if result.matched_count == 0:
        print("Task status not updated")
    else:
        print("Task status updated")
    
    return paper_id


async def save_extract_data(sample_paper_json):
    result = await db.papers.insert_one(sample_paper_json)
    return str(result.inserted_id)

# Async function to update task status
async def update_status(task_id, paper_id):
    result = await db.tasks.update_one(
        {"task_id": task_id},
        {"$set": {"status": "completed", "paper_id": paper_id}}
    )
    return result