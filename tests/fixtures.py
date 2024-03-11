WEATHER_API_CORRECT_DATA = {
    "coord": {"lon": 2.32, "lat": 48.858},
    "weather": [
        {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}
    ],
    "base": "stations",
    "main": {
        "temp": 8.19,
        "feels_like": 7.03,
        "temp_min": 6.07,
        "temp_max": 9.42,
        "pressure": 998,
        "humidity": 86,
    },
    "visibility": 10000,
    "wind": {"speed": 2.06, "deg": 220},
    "clouds": {"all": 0},
    "dt": 1710099501,
    "sys": {
        "type": 2,
        "id": 2012208,
        "country": "FR",
        "sunrise": 1710051241,
        "sunset": 1710092882,
    },
    "timezone": 3600,
    "id": 6545270,
    "name": "Palais-Royal",
    "cod": 200,
}

WEATHER_API_INCORRECT_DATA = {
    "coord": {"lon": 2.32, "lat": 48.858},
    "weather": [{"id": 800, "description": "clear sky", "icon": "01n"}],
    "base": "stations",
    "main": {
        "temp": 8.19,
        "temp_min": 6.07,
        "temp_max": 9.42,
        "pressure": 998,
        "humidity": 86,
    },
    "visibility": 10000,
    "wind": {"speed": 2.06, "deg": 220},
    "clouds": {"all": 0},
    "dt": 1710099501,
    "sys": {
        "type": 2,
        "id": 2012208,
        "country": "FR",
        "sunrise": 1710051241,
        "sunset": 1710092882,
    },
    "timezone": 3600,
    "id": 6545270,
    "cod": 200,
}
