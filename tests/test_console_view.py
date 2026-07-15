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


def test_prompt_sample_register_returns_all_none_when_sample_id_is_blank():
    with patch.object(console_view.console, "input", side_effect=[""]):
        result = console_view.prompt_sample_register()

    assert result == (None, None, None, None)


def test_prompt_order_submit_returns_all_none_when_customer_name_is_blank():
    with patch.object(console_view.console, "input", side_effect=[""]):
        result = console_view.prompt_order_submit()

    assert result == (None, None, None)


def test_prompt_search_keyword_returns_none_when_blank():
    with patch.object(console_view.console, "input", side_effect=[""]):
        result = console_view.prompt_search_keyword()

    assert result is None


def test_prompt_order_id_returns_none_when_blank():
    with patch.object(console_view.console, "input", side_effect=[""]):
        result = console_view.prompt_order_id()

    assert result is None
