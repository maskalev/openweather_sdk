from unittest import mock

import pytest

from openweather_sdk.exceptions import InvalidLocationException
from openweather_sdk.rest.geocoding import _GeocodingAPI
from tests.fixtures import GEOCODIND_API_DIRECT_DATA, GEOCODIND_API_ZIP_DATA


@pytest.fixture
def geocoding_api():
    yield _GeocodingAPI(appid="token", location="Paris", zip_code="75000,FR")


class TestGeocodingAPI:
    @mock.patch("openweather_sdk.rest.base._APIRequest._get_data")
    def test_direct(self, mock_get_data, geocoding_api):
        get_data_response = mock.Mock()
        get_data_response.return_value = []
        mock_get_data.side_effect = get_data_response
        with pytest.raises(InvalidLocationException):
            geocoding_api._direct()

        get_data_response.return_value = GEOCODIND_API_DIRECT_DATA
        mock_get_data.side_effect = get_data_response
        assert geocoding_api._direct() == GEOCODIND_API_DIRECT_DATA[0]

    @mock.patch("openweather_sdk.rest.base._APIRequest._get_data")
    def test_zip(self, mock_get_data, geocoding_api):
        get_data_response = mock.Mock()
        get_data_response.return_value = GEOCODIND_API_ZIP_DATA
        mock_get_data.side_effect = get_data_response
        assert geocoding_api._zip() == GEOCODIND_API_ZIP_DATA
