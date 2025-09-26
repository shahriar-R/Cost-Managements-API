import aioredis


REDIS_URL = f"redis://redis:6379"
redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)
