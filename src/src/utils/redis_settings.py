import os
from urllib.parse import urlparse
import redis

url = urlparse(os.environ.get("REDIS_TLS_URL"))
r = redis.Redis(host=url.hostname, port=url.port, username=url.username,
                password=url.password, ssl=True, ssl_cert_reqs=None)
