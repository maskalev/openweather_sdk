import inspect

from openweather_sdk.exceptions import AttributeValidationException


def _validate_selected_attr(value, possible_values):
    caller_function = inspect.currentframe().f_back.f_code
    caller_function_name = caller_function.co_name
    if value not in possible_values:
        raise AttributeValidationException(
            f"{caller_function_name} must be one of {', '.join(possible_values)}"
        )
    return value


def _validate_non_negative_integer_attr(value):
    caller_function = inspect.currentframe().f_back.f_code
    caller_function_name = caller_function.co_name
    if not isinstance(value, int) or value < 1:
        raise AttributeValidationException(
            f"{caller_function_name} must be non-negative integer"
        )
    return value
