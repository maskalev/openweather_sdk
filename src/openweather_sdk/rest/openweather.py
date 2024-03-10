from openweather_sdk.globals import _DOMAIN
from openweather_sdk.rest.base import _APIRequest


class _OpenWeather:
    def _health_check(self):
        return _APIRequest(_DOMAIN)._health_check()
