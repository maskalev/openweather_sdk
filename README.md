# OpenWeatherSDK

## Introduction

SDK for accessing to [OpenWeatherAPI](https://openweathermap.org/api) and
retrieving information about current weather conditions in a specified city.
The SDK can operate in two modes: *on-demand* and *polling*. In *on-demand*
mode (the default mode), API requests are made on user demand, while in the
*polling* mode, there is regular polling of the API for weather updates in the
saved (previously requested) cities.

## Contents

[Installation](#installation)

[Prerequisites](#prerequisites)

[Client initialization](#client-initialization)

[Cache](#cache)

[Additional arguments](#additional-arguments)

[Usage example](#usage-example)

[Errors](#errors)

## Installation

```python
pip install openweather_sdk
```

## Prerequisites

To work with the SDK, you need to obtain an access token for OpenWeatherAPI.
More information can be found on [FAQ page](https://openweathermap.org/faq)
("Get started" section -> "How to get an API key").

## Client initialization

The only required argument is [the access token](#prerequisites). Additionally,
if you need to modify the behavior of the SDK, you can pass
[additional arguments](#additional-arguments).

## Cache

Each client has its own cache, defined by the number of stored locations and
the Time-To-Live (TTL) of the information. In polling mode, the TTL determines
the API polling interval.

## Additional arguments

By default, the SDK operates in on-demand mode, returns information in English,
uses the metric system of measurements, has a cache size of 10 locations, and
the information remains valid for 10 minutes. You can modify this mode by
passing additional arguments during client initialization.

`mode` - determines the operating mode of the SDK. In on-demand mode, the SDK
makes requests to the API only upon client requests. In polling mode, the SDK
regularly polls the API. Defaults: on-demand. Available options: on-demand, polling.

`language` - determines the language for the output. Defaults: en. Available
options and more info see [here](https://openweathermap.org/current#multi).

`units` - determines the units of measurements for the output. Defaults:
metric. Available options and more info see
[here](https://openweathermap.org/current#data).

`cache_size` - determines the number of stored locations in cache. Defaults: 10.

`ttl` - determines the Time-To-Live of information in cache (in secs). Defaults:
600. 

## Usage example

```python
>>> from openweather_sdk import Client
>>> c = Client(token=<YOUR_TOKEN>)
>>> c.health_check()
200
>>> c.get_location_weather("Paris")
{'coord': {'lon': 2.32, 'lat': 48.859
    }, 'weather': [
        {'id': 300, 'main': 'Drizzle', 'description': 'light intensity drizzle', 'icon': '09d'
        },
        {'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'
        }
    ], 'base': 'stations', 'main': {'temp': 7.29, 'feels_like': 5.98, 'temp_min': 6.3, 'temp_max': 7.84, 'pressure': 993, 'humidity': 94
    }, 'visibility': 10000, 'wind': {'speed': 2.06, 'deg': 140
    }, 'rain': {'1h': 0.21
    }, 'clouds': {'all': 100
    }, 'dt': 1710053464, 'sys': {'type': 2, 'id': 2012208, 'country': 'FR', 'sunrise': 1710051241, 'sunset': 1710092881
    }, 'timezone': 3600, 'id': 6545270, 'name': 'Palais-Royal', 'cod': 200
}
>>> c.remove()
```

## Errors

Description of possible errors can be found on
[FAQ page](https://openweathermap.org/faq) ("API errors" section).
