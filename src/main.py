from fastapi import FastAPI, HTTPException, Request, status

from src.token_bucket_manager import TokenBucketManager
from src.client import get_client_ip

app = FastAPI()

rate_limiter = TokenBucketManager(max_tokens=3, refill_rate=1)


@app.get("/")
def root(request: Request):
    client_ip = get_client_ip(request)

    if not rate_limiter.allow_request(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
        )

    return {"message": "Hello World"}
