from openweather_sdk.exceptions import InvalidLocationException
from openweather_sdk.globals import _GEOCODING_API_VERSIONS
from openweather_sdk.rest.base import _APIRequest, _build_full_path, _create_path
from openweather_sdk.validators import _validate_attr


class _GeocodingAPI:
    """
    A class for creating data for path buildng to Geocoding API.
    See: https://openweathermap.org/api/geocoding-api.
    """

    def __init__(self, appid, location=None, zip_code=None, **kwargs):
        self.service_name = "geo"
        self.location = location or None
        self.zip_code = zip_code or None
        self.appid = appid
        self.version = kwargs.get("version", "1.0")
        self.limit = kwargs.get("limit", 1)

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = _validate_attr(value, _GEOCODING_API_VERSIONS)

    def _direct(self):
        """Get geographical data by using name of the location (city name or area name)."""
        end_point = "direct"
        query_params = {"q": self.location, "limit": self.limit, "appid": self.appid}
        path = _create_path(self.service_name, self.version, end_point)
        path_data = {"path": path, "query_params": query_params}
        full_path = _build_full_path(path_data)
        try:
            result = _APIRequest(full_path)._get_data()
            return result[0]
        except IndexError as e:
            raise InvalidLocationException

    def _zip(self, zip_code):
        """Get geographical coordinates (lon, lat) by using zip/post code"""
        return NotImplemented

    def _reverse(self):
        """Get name of the location (city name or area name) by using geografical coordinates (lon, lat)."""
        return NotImplemented
