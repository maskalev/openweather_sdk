import sys
from pathlib import Path
from unittest import mock

import pytest

__FILE_PATH__ = Path(__file__).parent.parent.absolute()
sys.path.append(f"{__FILE_PATH__}/src")

from fixtures import WEATHER_API_CORRECT_DATA

from openweather_sdk import Client
from openweather_sdk.exceptions import (ClientAlreadyExistsException,
                                        ClientDoesntExistException)


@pytest.fixture
def weather_client():
    test_token = "test_token"
    client = Client(token=test_token)
    yield client
    client.remove()


class TestClient:
    def test_client_initialization(self, weather_client):
        assert weather_client.is_alive
        assert weather_client.token in Client._active_tokens
        assert weather_client.mode == "on-demand"
        assert weather_client.language == "en"
        assert weather_client.units == "metric"
        assert weather_client.cache_size == 10
        assert weather_client.ttl == 600

    def test_remove_nonexistent_client(self):
        non_existent_client = Client(token="token")
        non_existent_client.remove()
        with pytest.raises(ClientDoesntExistException):
            non_existent_client.remove()

    def test_duplicate_token(self):
        with pytest.raises(ClientAlreadyExistsException):
            Client(token="token")
            Client(token="token")

    @mock.patch("openweather_sdk.rest.geocoding._GeocodingAPI._direct")
    @mock.patch("openweather_sdk.rest.weather._WeatherAPI._get_current_wheather")
    def test_get_location_weather(
        self, mock_get_weather, mock_get_coordinates, weather_client
    ):
        mock_response_coordinates = mock.Mock()
        mock_response_coordinates.return_value = {
            "name": "Paris",
            "lat": 48.8588897,
            "lon": 2.3200410217200766,
        }
        mock_get_coordinates.side_effect = mock_response_coordinates
        coordinates = weather_client._get_coordinates("Paris")
        assert coordinates == (2.32, 48.859)
        mock_response_weather = mock.Mock()
        mock_response_weather.return_value = WEATHER_API_CORRECT_DATA
        mock_get_weather.side_effect = mock_response_weather
        weather_data = weather_client._get_current_weather_coordinates(*coordinates)
        assert weather_data == WEATHER_API_CORRECT_DATA
