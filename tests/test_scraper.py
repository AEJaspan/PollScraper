#!/usr/bin/env python

"""Tests for `pollscraper` package."""

from bs4 import BeautifulSoup
from click.testing import CliRunner

from pollscraper import cli
from pollscraper.scraper import DataPipeline
import pandas as pd
from pathlib import Path
from root import ROOT_DIR


# def test_get_static_fixture(datafiles):
#     print(datafiles)
#     assert 1==1


# Test for DataPipeline class methods
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


# def test_clean_data(expected_html_response):
#     dp = DataPipeline()
#     table_data = expected_html_response
#     processed_data = dp.clean_data(table_data)
#     pd.testing.assert_frame_equal(processed_data, expected_html_response)


def test_command_line_interface(get_target_url):
    runner = CliRunner()
    url = get_target_url
    output = 'data/'
    commands = f'--quiet --url {url} --results_dir {ROOT_DIR}/{output}'
    result = runner.invoke(cli.main, commands)
    print(result.output)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert Path(f"{ROOT_DIR}/{output}/polls.csv").is_file()
    assert Path(f"{ROOT_DIR}/{output}/trends.csv").is_file()
