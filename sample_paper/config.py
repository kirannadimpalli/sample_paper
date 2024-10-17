
from redis import Redis
from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient('mongodb://root:test@mongo:27017')
db = client['sample_paper_db']
redis = Redis(host='redis', port=6379, db=0)

