
from redis import Redis
from motor.motor_asyncio import AsyncIOMotorClient
from celery import Celery


client = AsyncIOMotorClient('mongodb://root:test@mongo:27017')
db = client['paper_db']
redis = Redis(host='redis', port=6379, db=0)

celery_app = Celery(
    "sample_page",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)