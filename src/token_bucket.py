import time
from threading import Lock


class TokenBucket:
    def __init__(self, max_tokens: float, refill_rate: float):
        assert max_tokens > 0
        assert refill_rate > 0

        self.max_tokens = max_tokens
        self.refill_rate = refill_rate

        self.tokens = max_tokens
        self.last_refill_time = time.time()

        self.lock = Lock()

    def _refill(self) -> None:
        curr_time = time.time()
        diff_time = curr_time - self.last_refill_time

        missing_tokens = diff_time * self.refill_rate
        self.tokens = min(self.tokens + missing_tokens, self.max_tokens)

        self.last_refill_time = curr_time

    def allow_request(self) -> bool:
        with self.lock:
            self._refill()

            if self.tokens < 1.0:
                return False

            self.tokens -= 1.0
            return True
