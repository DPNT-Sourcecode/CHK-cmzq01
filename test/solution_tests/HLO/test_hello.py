import pytest

from solutions.HLO.hello_solution import hello


class TestHello:

    @pytest.mark.parametrize(
        "friend_name, expected_message",
        [
            ("tom", "Hello, World!"),
            ("another_friend", "Hello, World!"),
            ("and_another_friend", "Hello, World!"),
            ("", "Hello, World!"),
        ],
    )
    def test_hello(self, friend_name, expected_message):
        assert hello(friend_name) == expected_message

    @pytest.mark.parametrize(
        "friend_name, expected_exception_class",
        [
            (0.0, TypeError),
            ({"a": "b"}, TypeError),
            ({2, 3, 4}, TypeError),
        ],
    )
    def test_hello_exceptions(self, friend_name, expected_exception_class):
        with pytest.raises(expected_exception_class):
            hello(friend_name)


