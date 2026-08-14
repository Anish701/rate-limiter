import time
from pathlib import Path

import redis
from fastapi import HTTPException, Request, status

from src.client import get_client_ip

LUA_SCRIPT_FILE_PATH = Path("src/token_bucket.lua")
LUA_SCRIPT = LUA_SCRIPT_FILE_PATH.read_text()


class RedisTokenBucketManager:
    def __init__(
        self,
        redis_client: redis.Redis,
        max_tokens: float,
        refill_rate: float,
        key_prefix: str = "rate_limit",
    ):
        assert max_tokens > 0
        assert refill_rate > 0

        self.redis = redis_client
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.key_prefix = key_prefix

        self._script = self.redis.register_script(LUA_SCRIPT)

    def allow_request(self, ip: str, requested_tokens: float = 1.0) -> bool:
        key = f"{self.key_prefix}:{ip}"
        curr_time = time.time()

        result: bool = self._script(
            keys=[key],
            args=[self.max_tokens, self.refill_rate, curr_time, requested_tokens],
        )

        return result

    def __call__(self, request: Request) -> None:
        client_ip = get_client_ip(request)

        if not self.allow_request(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
            )
