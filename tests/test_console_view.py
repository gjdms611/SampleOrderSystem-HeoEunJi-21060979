from unittest.mock import patch

from view import console_view


def test_prompt_float_retries_after_invalid_input():
    with patch.object(console_view.console, "input", side_effect=["abc", "2.5"]):
        result = console_view.prompt_float("평균생산시간: ")

    assert result == 2.5


def test_prompt_int_retries_after_invalid_input():
    with patch.object(console_view.console, "input", side_effect=["abc", "10"]):
        result = console_view.prompt_int("수량: ")

    assert result == 10
