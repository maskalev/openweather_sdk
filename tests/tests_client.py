import sys
import warnings
from pathlib import Path
from unittest import mock

import pytest

__FILE_PATH__ = Path(__file__).parent.parent.absolute()
sys.path.append(f"{__FILE_PATH__}/src")

from fixtures import WEATHER_API_CORRECT_DATA

from openweather_sdk import Client
from openweather_sdk.exceptions import (
    AttributeValidationException,
    ClientAlreadyExistsException,
    ClientDoesntExistException,
    InvalidLocationException,
)

if sys.version_info < (3, 8):
    mock._magics.add("__round__")


@pytest.fixture
def weather_client():
    test_token = "test_token"
    client = Client(token=test_token)
    yield client
    if client.is_alive:
        client.remove()


class TestClient:
    def test_correct_client_initialization(self, weather_client):
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
            client = Client(token="token")
            Client(token="token")

        with pytest.raises(AttributeValidationException):
            Client(token="another_token", mode="mode")

        with pytest.raises(AttributeValidationException):
            Client(token="another_token", language="qq")

        with pytest.raises(AttributeValidationException):
            Client(token="another_token", units="units")

        with pytest.raises(AttributeValidationException):
            Client(token="another_token", cache_size=0)

        with pytest.raises(AttributeValidationException):
            Client(token="another_token", cache_size="1")

        with pytest.raises(AttributeValidationException):
            Client(token="another_token", ttl=0)

        with pytest.raises(AttributeValidationException):
            Client(token="another_token", ttl="1")

        Client(token="another_token")

    @mock.patch("openweather_sdk.rest.geocoding._GeocodingAPI._direct")
    @mock.patch("openweather_sdk.rest.weather._WeatherAPI._get_current_wheather")
    def test_get_location_current_weather(
        self, mock_get_weather, mock_get_coordinates, weather_client
    ):
        with warnings.catch_warnings(record=True) as w:
            weather_client.get_location_weather(location="Paris")
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)

        mock_response_coordinates = mock.Mock()
        mock_response_coordinates.return_value = {
            "name": "Paris",
            "lat": 48.8588897,
            "lon": 2.3200410217200766,
        }
        mock_get_coordinates.side_effect = mock_response_coordinates
        coordinates = weather_client._get_location_coordinates("Paris")
        assert coordinates == (2.32, 48.859)

        mock_response_weather = mock.Mock()
        mock_response_weather.return_value = WEATHER_API_CORRECT_DATA
        mock_get_weather.side_effect = mock_response_weather
        weather_data = weather_client._get_current_weather(*coordinates)
        assert weather_data == WEATHER_API_CORRECT_DATA

        with pytest.raises(InvalidLocationException):
            weather_client.get_location_weather(location=42)

        weather_client.remove()
        with pytest.raises(ClientDoesntExistException):
            weather_client.get_location_weather(location="Paris")

    @mock.patch("openweather_sdk.rest.geocoding._GeocodingAPI._zip")
    @mock.patch("openweather_sdk.rest.weather._WeatherAPI._get_current_wheather")
    def test_get_zip_current_weather(
        self, mock_get_weather, mock_get_coordinates, weather_client
    ):
        with warnings.catch_warnings(record=True) as w:
            weather_client.get_zip_weather(zip_code="75000,FR")
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)

        mock_response_coordinates = mock.Mock()
        mock_response_coordinates.return_value = {
            "zip": "75000",
            "name": "Paris",
            "lat": 48.8588897,
            "lon": 2.3200410217200766,
            "country": "FR",
        }
        mock_get_coordinates.side_effect = mock_response_coordinates
        coordinates = weather_client._get_zip_code_coordinates("75000,FR")
        assert coordinates == (2.32, 48.859)

        mock_response_weather = mock.Mock()
        mock_response_weather.return_value = WEATHER_API_CORRECT_DATA
        mock_get_weather.side_effect = mock_response_weather
        weather_data = weather_client._get_current_weather(*coordinates)
        assert weather_data == WEATHER_API_CORRECT_DATA

        with pytest.raises(InvalidLocationException):
            weather_client.get_zip_weather(zip_code=75000)

        weather_client.remove()
        with pytest.raises(ClientDoesntExistException):
            weather_client.get_zip_weather(zip_code="75000,FR")

    @mock.patch("openweather_sdk.rest.openweather._OpenWeather._health_check")
    def test_health_check(self, mock_health_check, weather_client):
        mock_response_health_check = mock.Mock()
        mock_response_health_check.return_value = 200
        mock_health_check.side_effect = mock_response_health_check
        status_code = weather_client.health_check()
        assert status_code == 200

        weather_client.remove()
        with pytest.raises(ClientDoesntExistException):
            weather_client.health_check()

    @mock.patch("openweather_sdk.rest.geocoding._GeocodingAPI._direct")
    @mock.patch("openweather_sdk.rest.weather._WeatherAPI._get_current_wheather")
    def test_current_weather(
        self, mock_get_weather, mock_get_coordinates, weather_client
    ):
        mock_response_coordinates = mock.Mock()
        mock_response_coordinates.return_value = {
            "name": "Paris",
            "lat": 48.8588897,
            "lon": 2.3200410217200766,
        }
        mock_get_coordinates.side_effect = mock_response_coordinates
        coordinates = weather_client._get_location_coordinates("Paris")
        assert coordinates == (2.32, 48.859)

        mock_response_weather = mock.Mock()
        mock_response_weather.return_value = WEATHER_API_CORRECT_DATA
        mock_get_weather.side_effect = mock_response_weather
        weather_data = weather_client._get_current_weather(*coordinates)
        assert weather_data == WEATHER_API_CORRECT_DATA

        with pytest.raises(InvalidLocationException):
            weather_client.current_weather()

        with pytest.raises(InvalidLocationException):
            weather_client.current_weather(zip_code=75000)

        with pytest.raises(InvalidLocationException):
            weather_client.current_weather(location=42)

        weather_client.remove()
        with pytest.raises(ClientDoesntExistException):
            weather_client.current_weather(zip_code="75000,FR")

    @mock.patch("openweather_sdk.rest.geocoding._GeocodingAPI._direct")
    @mock.patch("openweather_sdk.rest.forecast._ForecastAPI._get_forecast_5_days")
    def test_forecast_5_days(
        self, mock_get_weather, mock_get_coordinates, weather_client
    ):
        mock_response_coordinates = mock.Mock()
        mock_response_coordinates.return_value = {
            "name": "Paris",
            "lat": 48.8588897,
            "lon": 2.3200410217200766,
        }
        mock_get_coordinates.side_effect = mock_response_coordinates
        coordinates = weather_client._get_location_coordinates("Paris")
        assert coordinates == (2.32, 48.859)

        mock_response_weather = mock.Mock()
        mock_response_weather.return_value = WEATHER_API_CORRECT_DATA
        mock_get_weather.side_effect = mock_response_weather
        weather_data = weather_client._get_forecast_5_days(*coordinates)
        assert weather_data == WEATHER_API_CORRECT_DATA

        with pytest.raises(InvalidLocationException):
            weather_client.forecast_5_days()

        with pytest.raises(InvalidLocationException):
            weather_client.forecast_5_days(zip_code=75000)

        with pytest.raises(InvalidLocationException):
            weather_client.forecast_5_days(location=42)

        weather_client.remove()
        with pytest.raises(ClientDoesntExistException):
            weather_client.forecast_5_days(zip_code="75000,FR")

    @mock.patch("openweather_sdk.rest.geocoding._GeocodingAPI._direct")
    @mock.patch("openweather_sdk.rest.forecast._ForecastAPI._get_forecast_hourly")
    def test_forecast_hourly(
        self, mock_get_weather, mock_get_coordinates, weather_client
    ):
        mock_response_coordinates = mock.Mock()
        mock_response_coordinates.return_value = {
            "name": "Paris",
            "lat": 48.8588897,
            "lon": 2.3200410217200766,
        }
        mock_get_coordinates.side_effect = mock_response_coordinates
        coordinates = weather_client._get_location_coordinates("Paris")
        assert coordinates == (2.32, 48.859)

        mock_response_weather = mock.Mock()
        mock_response_weather.return_value = WEATHER_API_CORRECT_DATA
        mock_get_weather.side_effect = mock_response_weather
        weather_data = weather_client._get_forecast_hourly(*coordinates)
        assert weather_data == WEATHER_API_CORRECT_DATA

        with pytest.raises(InvalidLocationException):
            weather_client.forecast_hourly()

        with pytest.raises(InvalidLocationException):
            weather_client.forecast_hourly(zip_code=75000)

        with pytest.raises(InvalidLocationException):
            weather_client.forecast_hourly(location=42)

        weather_client.remove()
        with pytest.raises(ClientDoesntExistException):
            weather_client.forecast_hourly(zip_code="75000,FR")

    @mock.patch("openweather_sdk.rest.geocoding._GeocodingAPI._direct")
    @mock.patch("openweather_sdk.rest.forecast._ForecastAPI._get_forecast_daily_16_days")
    def test_forecast_daily_16_days(
        self, mock_get_weather, mock_get_coordinates, weather_client
    ):
        mock_response_coordinates = mock.Mock()
        mock_response_coordinates.return_value = {
            "name": "Paris",
            "lat": 48.8588897,
            "lon": 2.3200410217200766,
        }
        mock_get_coordinates.side_effect = mock_response_coordinates
        coordinates = weather_client._get_location_coordinates("Paris")
        assert coordinates == (2.32, 48.859)

        mock_response_weather = mock.Mock()
        mock_response_weather.return_value = WEATHER_API_CORRECT_DATA
        mock_get_weather.side_effect = mock_response_weather
        weather_data = weather_client._get_forecast_daily_16_days(*coordinates)
        assert weather_data == WEATHER_API_CORRECT_DATA

        with pytest.raises(InvalidLocationException):
            weather_client.forecast_daily_16_days()

        with pytest.raises(InvalidLocationException):
            weather_client.forecast_daily_16_days(zip_code=75000)

        with pytest.raises(InvalidLocationException):
            weather_client.forecast_daily_16_days(location=42)

        weather_client.remove()
        with pytest.raises(ClientDoesntExistException):
            weather_client.forecast_daily_16_days(zip_code="75000,FR")
