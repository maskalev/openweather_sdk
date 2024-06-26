import sys
from pathlib import Path

import freezegun
import pytest

from openweather_sdk.globals import _SPECIFIC_CACHES

__FILE_PATH__ = Path(__file__).parent.parent.absolute()
sys.path.append(f"{__FILE_PATH__}/src")

from fixtures import WEATHER_API_CORRECT_DATA

from openweather_sdk.cache import _ClientCache


@pytest.fixture
def client_cache():
    client_cache_ = {
        cache: _ClientCache(max_size=2, ttl=600, mode="on-demand")
        for cache in _SPECIFIC_CACHES
    }
    with freezegun.freeze_time("2024-01-01 00:00:00"):
        client_cache_["current_weather"]._add_info(
            2.32, 48.858, WEATHER_API_CORRECT_DATA
        )
    yield client_cache_


class TestCache:
    def test_increase_reduce_current_size(self, client_cache):
        assert client_cache["current_weather"].current_size == 1
        client_cache["current_weather"]._increase_current_size()
        assert client_cache["current_weather"].current_size == 2
        client_cache["current_weather"]._reduce_current_size()
        assert client_cache["current_weather"].current_size == 1

    def test_update_info(self, client_cache):
        assert client_cache["current_weather"]._get_time(2.32, 48.858) == 1704067200
        with freezegun.freeze_time("2024-01-02 00:00:00"):
            client_cache["current_weather"]._update_info(
                2.32, 48.858, WEATHER_API_CORRECT_DATA
            )
        assert client_cache["current_weather"].cache[2.32, 48.858]["time"] == 1704153600

    def test_is_relevant_info(self, client_cache):
        with freezegun.freeze_time("2024-01-01 00:10:00"):
            assert (
                client_cache["current_weather"]._is_relevant_info(2.32, 48.858) is True
            )
        with freezegun.freeze_time("2024-01-01 00:10:01"):
            assert (
                client_cache["current_weather"]._is_relevant_info(2.32, 48.858) is False
            )

    def test_remove_oldest_info(self, client_cache):
        with freezegun.freeze_time("2024-01-02 00:00:00"):
            client_cache["current_weather"]._add_info(
                2.32, 48.85, WEATHER_API_CORRECT_DATA
            )
        client_cache["current_weather"]._remove_oldest_info()
        assert client_cache["current_weather"].cache[2.32, 48.85]["time"] == 1704153600
        with pytest.raises(KeyError):
            assert (
                client_cache["current_weather"].cache[2.32, 48.858]["time"]
                == 1704067200
            )

    @freezegun.freeze_time("2024-01-01 00:00:00")
    def test_get_info(self, client_cache):
        assert (
            client_cache["current_weather"]._get_info(2.32, 48.858)
            == WEATHER_API_CORRECT_DATA
        )

    @freezegun.freeze_time("2024-01-01 00:00:00")
    def test_get_time(self, client_cache):
        assert client_cache["current_weather"]._get_time(2.32, 48.858) == 1704067200
