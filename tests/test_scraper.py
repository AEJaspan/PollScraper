#!/usr/bin/env python

"""Tests for `pollscraper` package."""
import pytest
import logging
import datetime
import pandas as pd
import requests

from bs4 import BeautifulSoup
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas.api.types import is_numeric_dtype as is_numeric
from pandas.api.types import is_string_dtype as is_string

from pollscraper.scraper import DataPipeline


LOGGER = logging.getLogger(__name__)
# class MockResponse:
#     def __init__(self, json_data, status_code):
#         self.json_data = json_data
#         self.status_code = status_code
#         self.elapsed = datetime.timedelta(seconds=1)

#     # mock json() method always returns a specific testing dictionary
#     def json(self):
#         return self.json_data

# def test_get_json(monkeypatch, caplog):
#     # Any arguments may be passed and mock_get() will always return our
#     # mocked object, which only has the .json() method.
#     def mock_get(*args, **kwargs):
#         return MockResponse({'mock_key': 'mock_value'}, 418)

#     # apply the monkeypatch for requests.get to mock_get
#     monkeypatch.setattr(requests, 'get', mock_get)
#     dp = DataPipeline()
#     url = 'https://fakeurl' # "https://www.example.com"
#     response = dp.fetch_html_content(url)
#     # app.get_json, which contains requests.get, uses the monkeypatch
#     # response = requests.get('https://fakeurl')
#     response_json = response.json()

#     assert response_json['mock_key'] == 'mock_value'
#     assert response.status_code == 418
#     assert response.elapsed.total_seconds() == 1

from unittest.mock import patch, Mock

@pytest.fixture
def http_instance():
    return DataPipeline()


# @patch('pollscraper.scraper.requests.Session')
# def test_fetch_html_content_success(mock_session, http_instance):
#     mock_response = Mock()
#     mock_response.status_code = 200
#     mock_response.raise_for_status.return_value = None
#     mock_session.return_value.get.return_value = mock_response

#     url = 'http://example.com'
#     response = http_instance.fetch_html_content(url)

#     assert response.status_code == 200




# @patch('pollscraper.scraper.requests.Session')
# def test_fetch_html_content_error(mock_session, http_instance, caplog):
#     mock_response = Mock()
#     mock_response.status_code = 404
#     # mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
#     # Make a dummy function that does nothing and use it as side effect
#     # def dummy_side_effect():
#     #     pass

#     # mock_response.raise_for_status.side_effect = dummy_side_effect

#     # mock_session.return_value.get.return_value = mock_response
#     # # mock_response.raise_for_status.return_value = None

#     # Use side_effect to replace the actual behavior of raise_for_status
#     def mock_raise_for_status():
#         pass

#     mock_response.raise_for_status.side_effect = mock_raise_for_status

#     mock_session.return_value.get.return_value = mock_response

#     url = 'http://httpbin.org/status/404'
#     with pytest.raises(requests.exceptions.HTTPError):
#         http_instance.fetch_html_content(url)
#     # Check if the log contains the expected error message
#     assert '404 Client Error' in caplog.text
#     # Ensure that raise_for_status was called
#     mock_response.raise_for_status.assert_called_once()






def test_fetch_html_content_success(http_instance, monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(requests.Session, 'get', mock_get)

    url = 'http://example.com'
    response = http_instance.fetch_html_content(url)

    assert response.status_code == 200

def test_fetch_html_content_error(http_instance, monkeypatch, caplog):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 404
            def raise_for_status(self):
                raise requests.exceptions.HTTPError()

        return MockResponse()

    monkeypatch.setattr(requests.Session, 'get', mock_get)

    url = 'https://fakeurl'
    with pytest.raises(requests.exceptions.HTTPError):
        http_instance.fetch_html_content(url)

    assert 'HTTPError' in caplog.text




















# # Test HTML retrieval
# def test_fetch_html_retreval(caplog):
#     # capture logger output
#     caplog.set_level(logging.WARNING)
#     dp = DataPipeline()
#     url = "https://www.example.com"
#     response = dp.fetch_html_content(url)
#     assert response.status_code == 200
#     url = 'c' # "https://www.example.com"
#     response = dp.fetch_html_content(url)
#     assert '4xx and 5xx' in caplog.text


# def test_get_json(monkeypatch, caplog):
#     # Any arguments may be passed and mock_get() will always return our
#     # mocked object, which only has the .json() method.
#     def mock_get(*args, **kwargs):
#         return MockResponse({'mock_key': 'mock_value'}, 418)

#     # apply the monkeypatch for requests.get to mock_get
#     monkeypatch.setattr(requests, 'get', mock_get)
#     dp = DataPipeline()
#     url = 'https://fakeurl' # "https://www.example.com"
#     response = dp.fetch_html_content(url)
#     # app.get_json, which contains requests.get, uses the monkeypatch
#     # response = requests.get('https://fakeurl')
#     response_json = response.json()

#     assert response_json['mock_key'] == 'mock_value'
#     assert response.status_code == 418
#     assert response.elapsed.total_seconds() == 1


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
