#!/usr/bin/env python

"""Tests for `pollscraper` package."""

import pytest
from bs4 import BeautifulSoup

from click.testing import CliRunner

from pollscraper import cli
from pollscraper.pollscraper import DataPipeline
import pandas as pd
import numpy as np

# Fixture for sample HTML content
@pytest.fixture
def sample_html_content():
    return """
    <table>
        <tr>
            <th>Header1</th>
            <th>Header2</th>
        </tr>
        <tr>
            <td>Data1</td>
            <td>Data2</td>
        </tr>
        <tr>
            <td>Data3</td>
            <td>Data4</td>
        </tr>
    </table>
    """

# Fixture for sample XML content
@pytest.fixture
def sample_xml_content():
    return """
    <root>
        <Keyword>
            <Term>Term1</Term>
            <Vocabulary>Vocab1</Vocabulary>
            <Definition>Definition1</Definition>
        </Keyword>
        <Keyword>
            <Term>Term2</Term>
            <Vocabulary>Vocab2</Vocabulary>
            <Definition>Definition2</Definition>
        </Keyword>
    </root>
    """

# Test for DataPipeline class methods
def test_fetch_html_content():
    dp = DataPipeline()
    url = "https://www.example.com"
    response = dp.fetch_html_content(url)
    assert response.status_code == 200

def test_extract_html_table_data(sample_html_content):
    dp = DataPipeline()
    soup = BeautifulSoup(sample_html_content, 'html.parser')
    table = soup.find('table')
    table_data = dp.extract_html_table_data(table)
    assert table_data == [['Header1', 'Header2'], ['Data1', 'Data2'], ['Data3', 'Data4']]

def test_parse_html_table(sample_html_content):
    dp = DataPipeline()
    table_data = dp.parse_html_table(sample_html_content)
    assert table_data == [['Header1', 'Header2'], ['Data1', 'Data2'], ['Data3', 'Data4']]

def test_parse_xml_table(sample_xml_content):
    dp = DataPipeline()
    xml_data = dp.parse_xml_table(sample_xml_content)
    expected_data = [
        {'Term': 'Term1', 'Vocabulary': 'Vocab1', 'Definition': 'Definition1'},
        {'Term': 'Term2', 'Vocabulary': 'Vocab2', 'Definition': 'Definition2'}
    ]
    assert xml_data == expected_data

def test_extract_table_data():
    dp = DataPipeline()
    csv_url = "https://www.example.com/sample.csv"
    html_url = "https://www.example.com/sample.html"
    xml_url = "https://www.example.com/sample.xml"
    
    csv_data = dp.extract_table_data(csv_url)
    assert isinstance(csv_data, pd.DataFrame)
    
    html_data = dp.extract_table_data(html_url)
    assert html_data == [['Header1', 'Header2'], ['Data1', 'Data2'], ['Data3', 'Data4']]
    
    xml_data = dp.extract_table_data(xml_url)
    expected_data = [
        {'Term': 'Term1', 'Vocabulary': 'Vocab1', 'Definition': 'Definition1'},
        {'Term': 'Term2', 'Vocabulary': 'Vocab2', 'Definition': 'Definition2'}
    ]
    assert xml_data == expected_data

def test_process_data():
    dp = DataPipeline()
    table_data = [['Header1', 'Header2'], ['Data1', 'Data2'], ['Data3', 'Data4']]
    processed_data = dp.process_data(table_data)
    expected_data = pd.DataFrame({'Header1': ['Data1', 'Data3'], 'Header2': ['Data2', 'Data4']})
    pd.testing.assert_frame_equal(processed_data, expected_data)

def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main, '--debug 10 --url https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html --results data/data.csv')
    print(result.output)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help           Show this message and exit.' in help_result.output
