import sys
from pathlib import Path

import pytest
from fixtures import WEATHER_API_CORRECT_DATA, WEATHER_API_INCORRECT_DATA

__FILE_PATH__ = Path(__file__).parent.parent.absolute()
sys.path.append(f"{__FILE_PATH__}/src")

from openweather_sdk import json_processor


class TestJSONProcessor:
    def test_handle_correct_data(self):
        input_data = WEATHER_API_CORRECT_DATA
        output_data = {
            "weather": {"main": "Clear", "description": "clear sky"},
            "temperature": {"temp": 8.19, "feels_like": 7.03},
            "visibility": 10000,
            "wind": {"speed": 2.06},
            "datatime": 1710099501,
            "sys": {"sunrise": 1710051241, "sunset": 1710092882},
            "timezone": 3600,
            "name": "Palais-Royal",
        }
        processor_compact_mode = json_processor._JSONProcessor(input_data)
        assert processor_compact_mode._handle() == output_data
        processor_full_mode = json_processor._JSONProcessor(
            input_data, compact_mode=False
        )
        assert processor_full_mode._handle() == input_data

    def test_handle_incorrect_data(self):
        input_data = WEATHER_API_INCORRECT_DATA
        output_data = {
            "weather": {"main": None, "description": "clear sky"},
            "temperature": {"temp": 8.19, "feels_like": None},
            "visibility": 10000,
            "wind": {"speed": 2.06},
            "datatime": 1710099501,
            "sys": {"sunrise": 1710051241, "sunset": 1710092882},
            "timezone": 3600,
            "name": None,
        }
        processor_compact_mode = json_processor._JSONProcessor(input_data)
        assert processor_compact_mode._handle() == output_data
        processor_full_mode = json_processor._JSONProcessor(
            input_data, compact_mode=False
        )
        assert processor_full_mode._handle() == input_data
