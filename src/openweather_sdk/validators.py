import inspect

from openweather_sdk.exceptions import AttributeValidationException


def _validate_attr(value, possible_values):
    caller_function = inspect.currentframe().f_back.f_code
    caller_function_name = caller_function.co_name
    if value not in possible_values:
        raise AttributeValidationException(caller_function_name, possible_values)
    return value
