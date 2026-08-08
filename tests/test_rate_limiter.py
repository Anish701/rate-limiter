import time

import pytest

from src.rate_limiter import TokenBucket


# Test that token overflow results in max_tokens
def test_refill_overflow() -> None:
    bucket = TokenBucket(max_tokens=5, refill_rate=4)

    bucket.tokens = 3.0

    time.sleep(1)
    bucket._refill()

    assert bucket.tokens == pytest.approx(5.0, abs=0.1)


# Test correct token calculation based on refill rate
def test_refill_regular() -> None:
    bucket = TokenBucket(max_tokens=10, refill_rate=1)

    bucket.tokens = 1.0

    time.sleep(3)
    bucket._refill()

    assert bucket.tokens == pytest.approx(4.0, abs=0.1)


# Test allow_request immediate denial when not enough tokens
def test_allow_request_deny() -> None:
    bucket = TokenBucket(max_tokens=5, refill_rate=1)

    bucket.tokens = 0.0

    assert not bucket.allow_request()


# Test allow_request immediate multiple calls
def test_allow_request_chain() -> None:
    bucket = TokenBucket(max_tokens=5, refill_rate=1)

    for _ in range(5):
        assert bucket.allow_request()

    assert not bucket.allow_request()