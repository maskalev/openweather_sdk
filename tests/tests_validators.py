from datetime import datetime, timedelta

import freezegun
import pytest

from openweather_sdk.exceptions import (
    AttributeValidationException,
    InvalidTimeException,
)
from openweather_sdk.validators import (
    _validate_non_negative_integer_attr,
    _validate_selected_attr,
    _validate_time,
)


class TestsValidators:
    def tests_validate_non_negative_integer_attr(self):
        with pytest.raises(AttributeValidationException):
            _validate_non_negative_integer_attr(-1)

        with pytest.raises(AttributeValidationException):
            _validate_non_negative_integer_attr(0)

        with pytest.raises(AttributeValidationException):
            _validate_non_negative_integer_attr("1")

        assert _validate_non_negative_integer_attr(1) == 1

    def tests_validate_selected_attr(self):
        possible_values = ("foo", "bar")
        with pytest.raises(AttributeValidationException):
            _validate_selected_attr("baz", possible_values)

        assert _validate_selected_attr("foo", possible_values) == "foo"

    def test_validate_time(self):
        with pytest.raises(InvalidTimeException):
            _validate_time(start=None, end=None)
        with pytest.raises(InvalidTimeException):
            _validate_time(start="1606435200", end=None)
        with pytest.raises(InvalidTimeException):
            _validate_time(start=1606435200, end="1606435200")
        with pytest.raises(InvalidTimeException):
            _validate_time(start=1606435201, end=1606435200)
        with pytest.raises(InvalidTimeException):
            _validate_time(start=1606435199, end=1606435200)
        cur_time = datetime.now()
        with freezegun.freeze_time(cur_time):
            with pytest.raises(InvalidTimeException):
                _validate_time(
                    start=cur_time + timedelta(seconds=1),
                    end=cur_time + timedelta(seconds=1),
                )
            with pytest.raises(InvalidTimeException):
                _validate_time(
                    start=cur_time,
                    end=cur_time + timedelta(seconds=1),
                )
        with freezegun.freeze_time(cur_time):
            _validate_time(start=1606435200, end=1606435200)
