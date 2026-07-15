import pytest

from model.production_calc import (
    calc_actual_production_qty,
    calc_shortage,
    calc_surplus,
    calc_total_production_time,
)


def test_calc_shortage():
    assert calc_shortage(order_qty=100, inventory_qty=30) == 70


def test_calc_actual_production_qty_ceil_not_evenly_divisible():
    # shortage=70, yield_rate=0.9 -> 70/0.9 = 77.77.. -> ceil -> 78
    assert calc_actual_production_qty(shortage=70, yield_rate=0.9) == 78


def test_calc_actual_production_qty_evenly_divisible():
    assert calc_actual_production_qty(shortage=70, yield_rate=1.0) == 70


def test_calc_total_production_time():
    assert calc_total_production_time(avg_production_time=2.5, actual_qty=78) == 195.0


def test_calc_surplus_not_evenly_divisible_is_positive():
    assert calc_surplus(actual_qty=78, shortage=70) == 8


def test_calc_surplus_evenly_divisible_is_zero():
    assert calc_surplus(actual_qty=70, shortage=70) == 0
