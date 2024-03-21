import freezegun
import pytest

from openweather_sdk.cache import _ClientCache
from tests.fixtures import WEATHER_API_CORRECT_DATA


@pytest.fixture
def client_cache():
    client_cache_ = _ClientCache(max_size=2, ttl=600, mode="on-demand")
    with freezegun.freeze_time("2024-01-01 00:00:00"):
        client_cache_._add_info(2.32, 48.858, WEATHER_API_CORRECT_DATA)
    yield client_cache_


class TestCache:
    def test_increase_reduce_current_size(self, client_cache):
        assert client_cache.current_size == 1
        client_cache._increase_current_size()
        assert client_cache.current_size == 2
        client_cache._reduce_current_size()
        assert client_cache.current_size == 1

    def test_update_info(self, client_cache):
        assert client_cache._get_time(2.32, 48.858) == 1704067200
        with freezegun.freeze_time("2024-01-02 00:00:00"):
            client_cache._update_info(2.32, 48.858, WEATHER_API_CORRECT_DATA)
        assert client_cache.cache[2.32, 48.858]["time"] == 1704153600

    def test_is_relevant_info(self, client_cache):
        with freezegun.freeze_time("2024-01-01 00:10:00"):
            assert client_cache._is_relevant_info(2.32, 48.858) is True
        with freezegun.freeze_time("2024-01-01 00:10:01"):
            assert client_cache._is_relevant_info(2.32, 48.858) is False

    def test_remove_oldest_info(self, client_cache):
        with freezegun.freeze_time("2024-01-02 00:00:00"):
            client_cache._add_info(2.32, 48.85, WEATHER_API_CORRECT_DATA)
        client_cache._remove_oldest_info()
        assert client_cache.cache[2.32, 48.85]["time"] == 1704153600
        with pytest.raises(KeyError):
            assert client_cache.cache[2.32, 48.858]["time"] == 1704067200

    @freezegun.freeze_time("2024-01-01 00:00:00")
    def test_get_info(self, client_cache):
        assert client_cache._get_info(2.32, 48.858) == WEATHER_API_CORRECT_DATA

    @freezegun.freeze_time("2024-01-01 00:00:00")
    def test_get_time(self, client_cache):
        assert client_cache._get_time(2.32, 48.858) == 1704067200
