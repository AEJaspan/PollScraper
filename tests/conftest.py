# content of tests/conftest.py
import pytest
import pandas as pd


@pytest.mark.datafiles('tests/test_scraper/expected_source_fixture.html')
@pytest.mark.datafiles('data/polls.example.csv')
@pytest.mark.datafiles('data/trends.example.csv')
@pytest.fixture
def get_target_url():
    return \
        'https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html'


@pytest.fixture
def sample_poll_data():
    return pd.read_csv('data/polls.example.csv', index_col=0)


@pytest.fixture
def sample_trends_data():
    return pd.read_csv('data/trends.example.csv', index_col=0)


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


@pytest.fixture
def expected_html_response():
    return [
        ['Header1', 'Header2'], ['Data1', 'Data2'], ['Data3', 'Data4']
        ]


@pytest.fixture
def expected_dataframe_response():
    return pd.DataFrame({
        'Header1': ['Data1', 'Data3'],
        'Header2': ['Data2', 'Data4']
    })
