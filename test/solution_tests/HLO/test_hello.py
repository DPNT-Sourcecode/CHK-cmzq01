import pytest

from solutions.HLO.hello_solution import hello


class TestHello:

    @pytest.mark.parametrize(
        "friend_name, expected_message",
        [
            ("tom", "Hello World!")
        ],
    )
    def test_hello(self, friend_name, expected_message):
        assert hello(friend_name) == expected_message
