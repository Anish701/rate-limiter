from fastapi import FastAPI, HTTPException, status

from src.token_bucket import TokenBucket

app = FastAPI()

rate_limiter = TokenBucket(max_tokens=3, refill_rate=1)


@app.get("/")
def root():
    if not rate_limiter.allow_request():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
        )

    return {"message": "Hello World"}
