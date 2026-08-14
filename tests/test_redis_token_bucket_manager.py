import time

import fakeredis
import pytest

from src.redis_token_bucket_manager import RedisTokenBucketManager

IP_NAME = "ip"


@pytest.fixture
def manager():
    fake_redis = fakeredis.FakeStrictRedis(decode_responses=True)
    return RedisTokenBucketManager(redis_client=fake_redis, max_tokens=5, refill_rate=1)


def test_allow_request_chain(manager) -> None:
    for _ in range(5):
        assert manager.allow_request(IP_NAME)

    assert not manager.allow_request(IP_NAME)


def test_refill_after_time(manager) -> None:
    for _ in range(5):
        assert manager.allow_request(IP_NAME)
    assert not manager.allow_request(IP_NAME)

    time.sleep(2)

    assert manager.allow_request(IP_NAME)
    assert manager.allow_request(IP_NAME)
    assert not manager.allow_request(IP_NAME)
