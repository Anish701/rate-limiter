from threading import Lock

from fastapi import HTTPException, Request, status

from src.client import get_client_ip
from src.token_bucket import TokenBucket


class TokenBucketManager:
    def __init__(self, max_tokens: float, refill_rate: float):
        assert max_tokens > 0
        assert refill_rate > 0

        self.max_tokens = max_tokens
        self.refill_rate = refill_rate

        self.buckets: dict[str, TokenBucket] = {}
        self.lock = Lock()

    def _get_bucket(self, ip: str) -> TokenBucket:
        if ip not in self.buckets:
            self.buckets[ip] = TokenBucket(
                max_tokens=self.max_tokens, refill_rate=self.refill_rate
            )

        return self.buckets.get(ip)

    def allow_request(self, ip: str) -> bool:
        with self.lock:
            ip_token_bucket = self._get_bucket(ip)
            return ip_token_bucket.allow_request()

    def __call__(self, request: Request) -> None:
        client_ip = get_client_ip(request)

        if not self.allow_request(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
            )
