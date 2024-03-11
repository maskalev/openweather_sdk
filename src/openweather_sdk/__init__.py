__version__ = "0.2.2"

import time
from threading import Thread

from openweather_sdk.cache import _ClientCache
from openweather_sdk.exceptions import (
    ClientAlreadyExistsException,
    ClientDoesntExistException,
    InvalidLocationException,
)
from openweather_sdk.globals import _BEHAVIORS, _LANGUAGES, _UNITS
from openweather_sdk.json_processor import _JSONProcessor
from openweather_sdk.rest.geocoding import _GeocodingAPI
from openweather_sdk.rest.openweather import _OpenWeather
from openweather_sdk.rest.weather import _WeatherAPI
from openweather_sdk.validators import _validate_attr


class Client:
    """
    A client for acessing to OpenWeather API.
    Client can works in 'on-demand' or 'polling' mode.
    In 'on-demand' mode, the client updates weather information solely upon
    user requests. In 'polling' mode, the SDK proactively requests fresh
    weather information for all stored locations, ensuring a zero-latency
    response for user requests.
    """

    _active_tokens = set()

    def __init__(
        self,
        token,
        mode="on-demand",
        language="en",
        units="metric",
        cache_size=10,
        ttl=600,
        **kwargs,
    ):
        """
        Сlient initialization.

        Args:
            token (str): unique OpenWeather API key. See on https://home.openweathermap.org/api_keys
            mode (str, optional): 'on-demand' or 'polling' mode.  Defaults to "on-demand".
            language (str, optional): language of the output. Current list see on https://openweathermap.org/current#multi. Defaults to "en".
            units (str, optional): units of measurement. See on https://openweathermap.org/current#data. Defaults to "metric".
            cache_size (int, optional): max size of cache. Defaults to 10.
            ttl (int, optional): the time (in sec) during which the information is considered relevant. Defaults to 600.
        """
        self.token = token
        self.mode = mode
        self.language = language
        self.units = units
        self.cache_size = cache_size
        self.ttl = ttl
        self.cache = _ClientCache(self.cache_size, self.ttl, self.mode)
        self._active_tokens.add(self.token)

        if self.mode == "polling":
            self.polling_thread = Thread(target=self._polling)
            self.polling_thread.start()

    @property
    def token(self):
        return self._token

    @property
    def mode(self):
        return self._behavior

    @property
    def language(self):
        return self._language

    @property
    def units(self):
        return self._units

    @token.setter
    def token(self, value):
        self._token = self._validate_token(value)

    @mode.setter
    def mode(self, value):
        self._behavior = _validate_attr(value, _BEHAVIORS)

    @language.setter
    def language(self, value):
        self._language = _validate_attr(value, _LANGUAGES)

    @units.setter
    def units(self, value):
        self._units = _validate_attr(value, _UNITS)

    @property
    def is_alive(self):
        return self.token in self._active_tokens

    def remove(self):
        """Remove the current client."""
        if self.is_alive:
            self._active_tokens.discard(self.token)
        else:
            raise ClientDoesntExistException
        if self.mode == "polling":
            self.polling_thread.join()

    def _validate_token(self, token):
        if token in self._active_tokens:
            raise ClientAlreadyExistsException
        return token

    def _get_coordinates(self, location):
        geocoding_api = _GeocodingAPI(location=location, appid=self.token)
        geo_info = geocoding_api._direct()
        lat = round(geo_info["lat"], 3)
        lon = round(geo_info["lon"], 3)
        return lon, lat

    def _get_current_weather_location(self, location):
        lon, lat = self._get_coordinates(location)
        return self._get_current_weather_coordinates(lon, lat)

    def _get_current_weather_coordinates(self, lon, lat):
        if self.cache._is_relevant_info(lon, lat):
            return self.cache._get_info(lon, lat)

        weather_api = _WeatherAPI(lon=lon, lat=lat, appid=self.token)
        weather = weather_api._get_current_wheather()

        self.cache._add_info(lon, lat, weather)
        return weather

    def _polling(self):
        while self.is_alive:
            time.sleep(self.cache.ttl)
            if not self.cache.cache:
                continue
            coordinates = list(self.cache.cache.keys())
            for lon, lat in coordinates:
                if (lon, lat) not in self.cache.cache:
                    continue
                weather_api = _WeatherAPI(lon=lon, lat=lat, appid=self.token)
                weather = weather_api._get_current_wheather()
                self.cache._update_info(lon, lat, weather)

    def get_location_weather(self, location, compact_mode=True):
        """Returns current weather in location (city name, state code (only for
        the US) and country code divided by comma. Please use ISO 3166 country
        codes).

        Args:
            location (str): city name, state code (only for the US) and country code divided by comma.
            compact_mode (bool, optional): Determines whether to return the response in a compact format.
        """
        if not self.is_alive:
            raise ClientDoesntExistException
        if not isinstance(location, str):
            raise InvalidLocationException
        weather = self._get_current_weather_location(location)
        json_processor = _JSONProcessor(weather, compact_mode)
        return json_processor._handle()

    def health_check(self):
        """Check if available API service."""
        if not self.is_alive:
            raise ClientDoesntExistException
        return _OpenWeather()._health_check()
