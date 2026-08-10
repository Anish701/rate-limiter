from src.token_bucket import TokenBucket
from src.token_bucket_manager import TokenBucketManager

IP_NAME = "ip"


def test_get_bucket_new() -> None:
    bucket_manager = TokenBucketManager(max_tokens=5, refill_rate=1)
    bucket_manager._get_bucket(IP_NAME)

    assert bucket_manager.buckets.get(IP_NAME) is not None


def test_get_bucket_existing() -> None:
    bucket_manager = TokenBucketManager(max_tokens=5, refill_rate=1)
    bucket_manager.buckets[IP_NAME] = TokenBucket(
        max_tokens=bucket_manager.max_tokens, refill_rate=bucket_manager.refill_rate
    )

    assert bucket_manager._get_bucket(IP_NAME) == bucket_manager.buckets[IP_NAME]


def test_allow_request_new_multiple() -> None:
    bucket_manager = TokenBucketManager(max_tokens=5, refill_rate=1)

    for _ in range(5):
        assert bucket_manager.allow_request(IP_NAME)

    assert not bucket_manager.allow_request(IP_NAME)


def test_allow_request_existing_multiple() -> None:
    bucket_manager = TokenBucketManager(max_tokens=5, refill_rate=1)
    bucket_manager.buckets[IP_NAME] = TokenBucket(
        max_tokens=bucket_manager.max_tokens, refill_rate=bucket_manager.refill_rate
    )

    for _ in range(5):
        assert bucket_manager.allow_request(IP_NAME)

    assert not bucket_manager.allow_request(IP_NAME)
