import time
from threading import Lock
from math import floor

'''
max_tokens = max tokens
tokens = current tokens
last_refill_time
refill_rate = tokens / s
'''

class TokenBucket:

    def __init__(self, max_tokens, refill_rate):
        assert max_tokens > 0
        assert refill_rate > 0

        self.max_tokens = max_tokens
        self.refill_rate = refill_rate

        self.tokens = max_tokens
        self.last_refill_time = time.time()

        self.lock = Lock()

    def _refill(self):
        curr_time = time.time()
        diff_time = curr_time - self.last_refill_time

        missing_tokens = floor(diff_time * self.refill_rate)
        self.tokens = max(self.tokens + missing_tokens, 10)

    def allow_request(self) -> bool: 
        return True