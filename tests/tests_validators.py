import pytest

from openweather_sdk.exceptions import AttributeValidationException
from openweather_sdk.validators import (
    _validate_non_negative_integer_attr,
    _validate_selected_attr,
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
