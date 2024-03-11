from openweather_sdk.globals import _WEATHER_API_VERSIONS
from openweather_sdk.rest.base import _APIRequest, _build_full_path, _create_path
from openweather_sdk.validators import _validate_attr


class _WeatherAPI:
    """
    A class for creating data for path buildng to Current Weather API.
    See: https://openweathermap.org/current.
    """

    def __init__(self, lon, lat, appid, **kwargs):
        self.service_name = "data"
        self.lat = lat
        self.lon = lon
        self.appid = appid
        self.version = kwargs.get("version", "2.5")
        self.units = kwargs.get("units", "metric")
        self.language = kwargs.get("language", "en")

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = _validate_attr(value, _WEATHER_API_VERSIONS)

    def _get_current_wheather(self):
        """Get the current weather at the specified point."""
        end_point = "weather"
        query_params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.appid,
            "units": self.units,
            "lang": self.language,
        }
        path = _create_path(self.service_name, self.version, end_point)
        path_data = {"path": path, "query_params": query_params}
        full_path = _build_full_path(path_data)
        return _APIRequest(full_path)._get_data()
