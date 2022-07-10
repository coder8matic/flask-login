import smartninja_redis
import os
import json

redis = smartninja_redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

# response = redis.set(name="user", value=json.dumps({
#     "name": "jan",
#     "surname": "plesko",
# }))

print(redis.get("user"))
print(redis.get("user_1"))
