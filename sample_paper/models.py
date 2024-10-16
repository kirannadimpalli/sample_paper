from motor.motor_asyncio import AsyncIOMotorClient
from .entity import SamplePaper

class MongoDB:
    def __init__(self, db_name: str, mongo_url: str):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]

    async def create_sample_paper(self, paper: SamplePaper) -> str:
        paper_dict = paper.dict()
        result = await self.db.papers.insert_one(paper_dict)
        return str(result.inserted_id)

    async def get_sample_paper(self, paper_id: str) -> SamplePaper:
        paper = await self.db.papers.find_one({"_id": ObjectId(paper_id)})
        return paper