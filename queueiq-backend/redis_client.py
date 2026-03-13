import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Setup Redis client
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def get_queue_length(department: str = "general") -> int:
    """Gets the current queue length for a department from Redis."""
    try:
        return redis_client.hlen(f"queue_state:{department}")
    except redis.ConnectionError:
        return 0 # Fallback if redis not running locally
