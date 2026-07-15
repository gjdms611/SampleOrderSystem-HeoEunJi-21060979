import pytest

from model.sample import Sample


def test_creates_sample_with_valid_values():
    sample = Sample(
        sample_id="S1",
        name="SampleA",
        avg_production_time=2.5,
        yield_rate=0.9,
    )

    assert sample.sample_id == "S1"
    assert sample.name == "SampleA"
    assert sample.avg_production_time == 2.5
    assert sample.yield_rate == 0.9


def test_rejects_non_positive_avg_production_time():
    with pytest.raises(ValueError):
        Sample(sample_id="S1", name="SampleA", avg_production_time=0, yield_rate=0.9)


def test_rejects_yield_rate_not_in_valid_range():
    with pytest.raises(ValueError):
        Sample(sample_id="S1", name="SampleA", avg_production_time=2.5, yield_rate=0)

    with pytest.raises(ValueError):
        Sample(sample_id="S1", name="SampleA", avg_production_time=2.5, yield_rate=1.1)
