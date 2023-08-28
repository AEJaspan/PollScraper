# content of tests/conftest.py
import pytest
import pandas as pd


@pytest.fixture
def datafiles():
    with open('tests/test_scraper/expected_source_fixture.html', 'r') as f:
        html_content = f.read()
    return html_content


@pytest.fixture
def expected_result():
    return pd.read_csv('tests/test_scraper/expected_result.csv',
                       index_col=0, parse_dates=['date'])


@pytest.fixture
def get_target_url():
    return \
        'https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html'


@pytest.fixture
def sample_poll_data():
    return pd.read_csv('data/polls.example.csv',
                       index_col=0, parse_dates=['date'])


@pytest.fixture
def candidate_dropout_data():
    return pd.read_csv('tests/test_trends/candidate_dropout_test.csv',
                       index_col=0, parse_dates=['date'])


@pytest.fixture
def candidate_late_join_data():
    return pd.read_csv('tests/test_trends/candidate_late_join_test.csv',
                       index_col=0, parse_dates=['date'])


@pytest.fixture
def large_gap_data():
    return pd.read_csv('tests/test_trends/large_gap_test.csv',
                       index_col=0, parse_dates=['date'])


@pytest.fixture
def opinion_shift_data():
    return pd.read_csv('tests/test_trends/opinion_shift_test.csv',
                       index_col=0, parse_dates=['date'])


@pytest.fixture
def sample_trends_data():
    return pd.read_csv('data/trends.example.csv',
                       index_col=0, parse_dates=['date'])


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
