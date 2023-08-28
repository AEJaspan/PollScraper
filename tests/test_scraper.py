#!/usr/bin/env python

"""Tests for `pollscraper` package."""

from bs4 import BeautifulSoup

from pollscraper.scraper import DataPipeline
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas.api.types import is_numeric_dtype as is_numeric
from pandas.api.types import is_string_dtype as is_string


def test_data_pipeline_with_html(datafiles, expected_result):
    dp = DataPipeline()

    table_df = dp.parse_html_table(datafiles)
    processed_data = dp.clean_data(table_df)

    # Data type validation
    expected_dtypes = {
        'date': is_datetime,
        'pollster': is_string,
        'n': is_numeric
    }
    for col, dtype in expected_dtypes.items():
        assert dtype(processed_data[col])

    assert processed_data[processed_data[col] > 0].all().all()

    # Compare processed_data with expected_df
    pd.testing.assert_frame_equal(processed_data, expected_result)


# Test HTML retrieval
def test_fetch_html_content(get_target_url):
    dp = DataPipeline()
    url = "https://www.example.com"
    response = dp.fetch_html_content(url)
    assert response.status_code == 200
    url = get_target_url
    response = dp.fetch_html_content(url)
    assert response.status_code == 200


def test_extract_html_table_data(sample_html_content, expected_html_response):
    dp = DataPipeline()
    soup = BeautifulSoup(sample_html_content, 'html.parser')
    table = soup.find('table')
    table_data = dp.extract_html_table_data(table)
    assert table_data == expected_html_response


def test_parse_html_table(sample_html_content, expected_dataframe_response):
    dp = DataPipeline()
    table_data = dp.parse_html_table(sample_html_content)
    pd.testing.assert_frame_equal(table_data, expected_dataframe_response)
