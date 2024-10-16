from app import app
from entity import SamplePaper
from config import db, redis


# @app.post("/papers", response_model=dict)
# async def create_paper(paper: SamplePaper):
#     breakpoint()
#     result = await db.papers.insert_one(paper.dict())
#     return {"paper_id": str(result.inserted_id)}



