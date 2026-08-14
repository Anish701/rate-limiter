import redis
from fastapi import Depends, FastAPI

# from src.token_bucket_manager import TokenBucketManager
from src.redis_token_bucket_manager import RedisTokenBucketManager

app = FastAPI()

# Option for in-memory rate limiter
# rate_limiter = TokenBucketManager(max_tokens=3, refill_rate=1)

# Option for redis rate limiter
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
rate_limiter = RedisTokenBucketManager(
    redis_client=redis_client,
    max_tokens=3,
    refill_rate=1,
    key_prefix="redis_rate_limit",
)


@app.get("/", dependencies=[Depends(rate_limiter)])
def root():
    return {"message": "Hello World"}
