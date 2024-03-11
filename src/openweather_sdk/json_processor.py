class _JSONProcessor:
    def __init__(self, json_data, compact_mode=True):
        self.json_data = json_data
        self.compact_mode = compact_mode

    def _get_nested_key(self, keys, current_value=None):
        current_value = current_value or self.json_data
        for key in keys:
            if isinstance(current_value, list):
                try:
                    current_value = current_value[key]
                except IndexError:
                    return None
            else:
                current_value = current_value.get(key)
        return current_value

    def _handle(self):
        if self.compact_mode:
            return {
                "weather": {
                    "main": self._get_nested_key(["weather", 0, "main"]),
                    "description": self._get_nested_key(["weather", 0, "description"]),
                },
                "temperature": {
                    "temp": self._get_nested_key(["main", "temp"]),
                    "feels_like": self._get_nested_key(["main", "feels_like"]),
                },
                "visibility": self._get_nested_key(["visibility"]),
                "wind": {
                    "speed": self._get_nested_key(["wind", "speed"]),
                },
                "datatime": self._get_nested_key(["dt"]),
                "sys": {
                    "sunrise": self._get_nested_key(["sys", "sunrise"]),
                    "sunset": self._get_nested_key(["sys", "sunset"]),
                },
                "timezone": self._get_nested_key(["timezone"]),
                "name": self._get_nested_key(["name"]),
            }
        return self.json_data
