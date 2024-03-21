import json
from unittest import mock

import pytest
import requests

from openweather_sdk.exceptions import BadResponseException
from openweather_sdk.globals import _DOMAIN
from openweather_sdk.rest.base import (
    _APIRequest,
    _build_full_path,
    _create_params,
    _create_path,
)
from tests.fixtures import WEATHER_API_CORRECT_DATA


@pytest.fixture
def api_request():
    yield _APIRequest("path")


class TestAPIRequest:
    @mock.patch("requests.get")
    def test_get_correct(self, mock_requests_get, api_request):
        mock_response = mock.Mock()
        response = requests.models.Response()
        response.status_code = 200
        response._content = json.dumps(WEATHER_API_CORRECT_DATA)
        mock_response.return_value = response
        mock_requests_get.side_effect = mock_response
        assert api_request._get()._content == json.dumps(WEATHER_API_CORRECT_DATA)

    @mock.patch("requests.get")
    def test_get_incorrect(self, mock_requests_get, api_request):
        mock_response = mock.Mock()
        response = requests.models.Response()
        response.status_code = 404
        response._content = json.dumps({"message": "Not Found"})
        mock_response.return_value = response
        mock_requests_get.side_effect = mock_response
        with pytest.raises(BadResponseException):
            api_request._get()

    @mock.patch("openweather_sdk.rest.base._APIRequest._get")
    def test_get_data(self, mock_requests_get, api_request):
        mock_response = mock.Mock()
        response = requests.models.Response()
        response.status_code = 200
        response._content = json.dumps(WEATHER_API_CORRECT_DATA)
        mock_response.return_value = response
        mock_requests_get.side_effect = mock_response
        assert api_request._get_data() == WEATHER_API_CORRECT_DATA

    @mock.patch("openweather_sdk.rest.base._APIRequest._get")
    def test_health_check(self, mock_requests_get, api_request):
        mock_response = mock.Mock()
        response = requests.models.Response()
        response.status_code = 200
        mock_response.return_value = response
        mock_requests_get.side_effect = mock_response
        assert api_request._health_check() == 200


def test_create_params():
    query_params = {"param1": "value1", "param2": "value2"}
    assert _create_params(query_params) == "param1=value1&param2=value2"


def test_build_full_path():
    path_data = {
        "path": _DOMAIN,
        "query_params": {"param1": "value1", "param2": "value2"},
    }
    assert _build_full_path(path_data) == f"{_DOMAIN}?param1=value1&param2=value2"


def test_create_path():
    segments = ("segment1", "segment2")
    assert _create_path(*segments) == f"{_DOMAIN}segment1/segment2"
