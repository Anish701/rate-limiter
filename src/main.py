from fastapi import Depends, FastAPI

from src.token_bucket_manager import TokenBucketManager

app = FastAPI()

rate_limiter = TokenBucketManager(max_tokens=3, refill_rate=1)


@app.get("/", dependencies=[Depends(rate_limiter)])
def root():
    return {"message": "Hello World"}
