from threading import Lock

from token_bucket import TokenBucket


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
