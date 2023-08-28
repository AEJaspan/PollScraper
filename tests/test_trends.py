from pollscraper.trends import PollTrend
# import pytest


def test_calculate_trends(sample_poll_data):
    trends, outliers_avg, outliers_poll = PollTrend\
        .calculate_trends(sample_poll_data, n_sigma=2)

    assert trends.shape[0]*.05 > outliers_avg.shape[0]
    assert trends.shape[0]*.1 > outliers_poll.shape[0]


def test_candidate_dropout_trends(candidate_dropout_data):
    trends, outliers_avg, outliers_poll = PollTrend\
        .calculate_trends(candidate_dropout_data, n_sigma=2)

    assert trends.shape[0]*.05 > outliers_avg.shape[0]
    assert trends.shape[0]*.1 > outliers_poll.shape[0]


def test_candidate_late_join_trends(candidate_late_join_data):
    trends, outliers_avg, outliers_poll = PollTrend\
        .calculate_trends(candidate_late_join_data, n_sigma=2)

    assert trends.shape[0]*.05 > outliers_avg.shape[0]
    assert trends.shape[0]*.1 > outliers_poll.shape[0]


def test_large_gap_trends(large_gap_data):
    trends, outliers_avg, outliers_poll = PollTrend\
        .calculate_trends(large_gap_data, n_sigma=2)

    assert trends.shape[0]*.05 > outliers_avg.shape[0]
    assert trends.shape[0]*.1 > outliers_poll.shape[0]


def test_opinion_shift_trends(opinion_shift_data):
    trends, outliers_avg, outliers_poll = PollTrend\
        .calculate_trends(opinion_shift_data, n_sigma=2)

    assert trends.shape[0]*.05 > outliers_avg.shape[0]
    assert trends.shape[0]*.1 > outliers_poll.shape[0]
