import smartninja_redis
import os

redis = smartninja_redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
