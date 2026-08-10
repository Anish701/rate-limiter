from fastapi import FastAPI, HTTPException, Request, status

from src.token_bucket_manager import TokenBucketManager

app = FastAPI()

rate_limiter = TokenBucketManager(max_tokens=3, refill_rate=1)


@app.get("/")
def root(request: Request):
    if not rate_limiter.allow_request(request.client.host):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
        )

    return {"message": "Hello World"}
