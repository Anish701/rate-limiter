from src.token_bucket import TokenBucket
from src.token_bucket_manager import TokenBucketManager

IP_NAME = "ip"


def test_get_bucket_new() -> None:
    bucketManager = TokenBucketManager(max_tokens=5, refill_rate=1)
    bucketManager._get_bucket(IP_NAME)

    assert bucketManager.buckets.get(IP_NAME) is not None


def test_get_bucket_existing() -> None:
    bucketManager = TokenBucketManager(max_tokens=5, refill_rate=1)
    bucketManager.buckets[IP_NAME] = TokenBucket(
        max_tokens=bucketManager.max_tokens, refill_rate=bucketManager.refill_rate
    )

    assert bucketManager._get_bucket(IP_NAME) == bucketManager.buckets[IP_NAME]


def test_allow_request_new_multiple() -> None:
    bucketManager = TokenBucketManager(max_tokens=5, refill_rate=1)

    for _ in range(5):
        assert bucketManager.allow_request(IP_NAME)

    assert not bucketManager.allow_request(IP_NAME)


def test_allow_request_existing_multiple() -> None:
    bucketManager = TokenBucketManager(max_tokens=5, refill_rate=1)
    bucketManager.buckets[IP_NAME] = TokenBucket(
        max_tokens=bucketManager.max_tokens, refill_rate=bucketManager.refill_rate
    )

    for _ in range(5):
        assert bucketManager.allow_request(IP_NAME)

    assert not bucketManager.allow_request(IP_NAME)
