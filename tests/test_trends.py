from pollscraper.trends import PollTrend
# import pytest


def test_calculate_trends(sample_poll_data):
    trends = PollTrend.calculate_trends(sample_poll_data)

    assert not trends.empty
