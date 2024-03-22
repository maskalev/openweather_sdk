import logging

from openweather_sdk.logger_filters import TokenFilter


class TestTokenFilter:
    def test_token_filter(self):
        record = logging.LogRecord(
            name="name",
            level=logging.INFO,
            pathname="pathname",
            lineno=0,
            msg="/data/2.5/weather?lat=48.859&lon=2.32&appid=token",
            exc_info=None,
            args=(),
        )
        res = TokenFilter().filter(record)
        assert record.msg == "/data/2.5/weather?lat=48.859&lon=2.32&appid=..."
        assert res is True
