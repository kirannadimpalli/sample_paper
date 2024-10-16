from app import app
from entity import SamplePaper
from config import db, redis


@app.post("/papers")
async def create_paper(paper: SamplePaper):
    paper_dict = paper.dict()
    result = await db.papers.insert_one(paper_dict)
    return {"paper_id": str(result.inserted_id)}



@app.get("/papers/{paper_id}")
async def get_paper(paper_id: str):
    cached_paper = redis.get(paper_id)
    if cached_paper:
        return cached_paper
    
    paper = await db.papers.find_one({"_id": paper_id})
    if paper:
        redis.set(paper_id, paper)
        return paper
    return {"error": "Paper not found"}, 404