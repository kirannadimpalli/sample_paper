from fastapi import FastAPI
from .entity import SamplePaper, TextInput
from .config import db
from fastapi import HTTPException
from redis import Redis
import json
from bson import ObjectId, json_util
from fastapi import Body
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from .task import process_pdf_task
import uuid
from .utils import extract_pdf_data

app = FastAPI()

redis = Redis(host='redis', port=6379, db=0)

import time

def connect_to_redis(max_retries=5, wait=5):
    redis = None
    for attempt in range(max_retries):
        try:
            redis = Redis(host='redis', port=6379, db=0)
            redis.ping()  # Test the connection
            print("Connected to Redis")
            break
        except Exception as e:
            print(f"Redis connection error: {e}, retrying...")
            time.sleep(wait)  # Wait before retrying
    if redis is None:
        print("Could not connect to Redis after retries")
    return redis

redis = connect_to_redis()

@app.get("/")
def read_root():
    return {"message": "welcome to application"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/papers", response_model=dict)
async def create_paper(paper: SamplePaper):
    result = await db.papers.insert_one(paper.dict())
    return {"paper_id": str(result.inserted_id)}



@app.get("/papers/{paper_id}")
async def get_paper(paper_id: str):
    try:
        if redis is None:
            raise HTTPException(status_code=500, detail="Redis not reachable")
        
        print(f"Fetching paper from Redis for ID: {paper_id}")
        cached_paper = redis.get(paper_id)

        if cached_paper:
            print("Paper found in cache.")
            return json.loads(cached_paper)  # Deserialize from JSON

        # Convert paper_id to ObjectId if needed
        try:
            object_id = ObjectId(paper_id)
            print("this is object id", object_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        # Fetch paper from MongoDB
        paper = await db.papers.find_one({"_id": object_id})
        print("paper is", paper)
        if paper:
            # Convert the document to a JSON serializable format before caching and returning
            paper_serializable = json.loads(json_util.dumps(paper))
            print(paper_serializable, "<-- it is a paper serialize")
            
            # Cache the serialized document in Redis
            redis.set(paper_id, json.dumps(paper_serializable))  
            
            return paper_serializable

        return {"message": "paper is not found"}

    except Exception as e:
        print(f"Error fetching paper: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.put("/papers/{paper_id}", response_model=dict)
async def update_paper(paper_id: str, update_data: dict = Body(...)):
    """
    Update an existing paper with partial updates supported.
    """
    try:
        if redis is None:
            raise HTTPException(status_code=500, detail="Redis not reachable")
        
        # Convert paper_id to ObjectId
        try:
            object_id = ObjectId(paper_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        # Perform partial update using MongoDB's update_one method
        update_result = await db.papers.update_one(
            {"_id": object_id},  # Match document by _id
            {"$set": update_data}  # Apply the update
        )

        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Paper not found")

        # Invalidate cache for this paper if it's cached
        redis.delete(paper_id)

        return {"message": "Paper updated successfully"}

    except Exception as e:
        print(f"Error updating paper: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.delete("/papers/{paper_id}", response_model=dict)
async def delete_paper(paper_id: str):
    """
    Delete a paper by paper_id.
    """
    try:
        if redis is None:
            raise HTTPException(status_code=500, detail="Redis not reachable")
        
        # Convert paper_id to ObjectId
        try:
            object_id = ObjectId(paper_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        # Delete the paper from MongoDB
        delete_result = await db.papers.delete_one({"_id": object_id})

        if delete_result.deleted_count == 0:
           return {"message": "it might be deleted or given id not exist"}

        # Remove from cache if it exists
        redis.delete(paper_id)

        return {"message": "Paper deleted successfully"}

    except Exception as e:
        print(f"Error deleting paper: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.post("/extract/pdf")
async def extract_pdf(file: UploadFile = File(...)):
    pdf_content = await file.read()  # Read the file content

    # Create a new task with status 'pending'
    task_id = str(uuid.uuid4())
    task_data = {"task_id": task_id, "status": "pending", "paper_id": None}
    await db.tasks.insert_one(task_data)

    # Encode the binary PDF content to base64 before passing to Celery
    pdf_content_base64 = base64.b64encode(pdf_content).decode('utf-8')

    # Asynchronously process the PDF in the background
    process_pdf_task.delay(task_id, pdf_content_base64)

    # Return the task ID
    return {"task_id": task_id, "status": "pending"}

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task = await db.tasks.find_one({"task_id": task_id})
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task_id": task["task_id"], "status": task["status"], "paper_id": task.get("paper_id")}



@app.post("/extract/text", response_model=dict)
async def extract_text(input: TextInput):
    """
    Accepts plain text input, processes it with Gemini, and returns it in JSON format.
    """
    try:
        # Process the input text using the Gemini model
        processed_data = extract_pdf_data(input.text)

        # Return the structured JSON format
        return processed_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")