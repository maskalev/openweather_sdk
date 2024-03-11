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

[Weather request](#weather-request)

[Description of response formats](#description-of-response-formats)

[Usage example](#usage-example)

[Errors](#errors)

## Installation

```python
pip install msklv-openweather-sdk
```

## Prerequisites

To work with the SDK, you need to obtain an access token for OpenWeatherAPI.
More information can be found on [FAQ page](https://openweathermap.org/faq)
("Get started" section -> "How to get an API key").

## Client initialization

The only required argument is [the access token](#prerequisites).

By default, the SDK operates in on-demand mode, returns information in English,
uses the metric system of measurements, has a cache size of 10 locations, and
the information remains valid for 10 minutes. You can modify this mode by
passing additional arguments during client initialization.

Additionally, if you need to modify the behavior of the SDK, you can pass
[additional arguments](#additional-arguments).

### Additional arguments

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

## Cache

Each client has its own cache, defined by the number of stored locations and
the Time-To-Live (TTL) of the information. In polling mode, the TTL determines
the API polling interval.

## Weather request

Currently, handling requests for current weather by location name is
implemented. By default, the response is returned in a compact format. You can
change this behavior by passing an [additional argument](#additional-arguments-1).

### Additional arguments

`compact_mode` - determines whether to return the response in a compact format.
Defaults: True.

## Description of response formats

### Compact format (used by default)

```json
{
    "weather": {
        "main": "Clear",
        "description": "clear sky"
    }, 
    "temperature": {
        "temp": 8.19,
        "feels_like": 7.03
    }, 
    "visibility": 10000, 
    "wind": {
        "speed": 2.06
    }, 
    "datatime": 1710099501, 
    "sys": {
        "sunrise": 1710051241,
        "sunset": 1710092882
    }, 
    "timezone": 3600, 
    "name": "Palais-Royal"
}
```

`weather.main` - group of weather parameters (Rain, Snow, Clouds etc.).

`weather.description` - weather condition within the group. More info see
[here](https://openweathermap.org/weather-conditions).

`temperature.temp` - temperature. Unit Standart: Kelvin, Metric: Celsius,
Imperial: Fahrenheit.

`temperature.feels_like` - temperature. This temperature parameter accounts for
the human perception of weather. Unit Standart: Kelvin, Metric: Celsius,
Imperial: Fahrenheit.

`visibility` - visibility, meter. The maximum value of the visibility is 10 km.

`wind.speed` - wind speed. Unit Standart: meter/sec, Metric: meter/sec,
Imperial: miles/hour.

`datatime` - time of data calculation, unix, UTC.

`sys.sunrise` - sunrise time, unix, UTC.

`sys.sunset` - sunset time, unix, UTC.

`timezone` - shift in seconds from UTC.

`name` - city name.

### Full format

```json
{
    "coord": {
        "lon": 2.32,
        "lat": 48.858
    },
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01n"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 8.19,
        "feels_like": 7.03,
        "temp_min": 6.07,
        "temp_max": 9.42,
        "pressure": 998,
        "humidity": 86
    },
    "visibility": 10000,
    "wind": {
        "speed": 2.06,
        "deg": 220
    },
    "clouds": {
        "all": 0
    },
    "dt": 1710099501,
    "sys": {
        "type": 2,
        "id": 2012208,
        "country": "FR",
        "sunrise": 1710051241,
        "sunset": 1710092882
    },
    "timezone": 3600,
    "id": 6545270,
    "name": "Palais-Royal",
    "cod": 200
}
```

Description of full format see
[here](https://openweathermap.org/current#fields_json)


## Usage example

```python
>>> from openweather_sdk import Client
>>> c = Client(token=<YOUR_TOKEN>)
>>> c.health_check()
200
>>> c.get_location_weather("Paris")
{
    "weather": {
        "main": "Clear",
        "description": "clear sky"
    }, 
    "temperature": {
        "temp": 8.19,
        "feels_like": 7.03
    }, 
    "visibility": 10000, 
    "wind": {
        "speed": 2.06
    }, 
    "datatime": 1710099501, 
    "sys": {
        "sunrise": 1710051241,
        "sunset": 1710092882
    }, 
    "timezone": 3600, 
    "name": "Palais-Royal"
}
>>> c.get_location_weather("Paris", compact_mode=False)
{
    "coord": {
        "lon": 2.32,
        "lat": 48.858
    },
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01n"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 8.19,
        "feels_like": 7.03,
        "temp_min": 6.07,
        "temp_max": 9.42,
        "pressure": 998,
        "humidity": 86
    },
    "visibility": 10000,
    "wind": {
        "speed": 2.06,
        "deg": 220
    },
    "clouds": {
        "all": 0
    },
    "dt": 1710099501,
    "sys": {
        "type": 2,
        "id": 2012208,
        "country": "FR",
        "sunrise": 1710051241,
        "sunset": 1710092882},
    "timezone": 3600,
    "id": 6545270,
    "name": "Palais-Royal",
    "cod": 200
}
>>> c.remove()
```

## Errors

Description of possible errors can be found on
[FAQ page](https://openweathermap.org/faq) ("API errors" section).
