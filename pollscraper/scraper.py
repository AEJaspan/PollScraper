"""Main module."""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import logging
from urlpath import URL
from pollscraper import logger
from requests.adapters import HTTPAdapter, Retry


class DataPipeline:
    """
    DataPipeline class for processing and transforming data.

    This class provides methods to load data from a source,
    transform it, and save it to a destination.

    Attributes:
        source (str): The path to the source file.
        destination (str): The path to the destination file.
        logger (logger.Logger): Logger instance for logging messages.
    """

    def __init__(self, http_n_retries=5,
                 http_connection_timeout=5,
                 http_read_timeout=30) -> None:
        """
        Initialize the DataPipeline object.

        For timeout policy, see:
        https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
        For retry options, see:
        https://requests.readthedocs.io/en/latest/user/advanced/#example-automatic-retries

        Args:
            http_n_retries (int, optional): Number of attempts to connect to.
                                            Defaults to 5.
            http_connection_timeout (int, optional): number of seconds Requests
                                                     will wait for your client
                                                     to establish a connection
                                                     to a remote machine.
                                                     Defaults to 5.
            http_read_timeout (int, optional): number of seconds the client
                                               will wait for the server to
                                               send a response. Defaults to 30.
        """
        self.common_header_mapping = {
            'Date': 'date',
            'Pollster': 'pollster',
            'Sample': 'n'
        }
        self.session = requests.Session()
        self.retries = Retry(total=5,
                             backoff_factor=0.1,
                             status_forcelist=[
                                    500,
                                    502,
                                    503,
                                    504
                                 ])
        self.adapter = HTTPAdapter(max_retries=self.retries)
        self.session.mount('http://', self.adapter)
        timeout_connect = 5
        timeout_read = 30
        self.timeout_policy = (timeout_connect, timeout_read)
        self.headers = {'Accept-Encoding': 'identity'}
        logger.debug("Data Pipeline Initialised.")

    def fetch_html_content(self, url):
        """
        Fetch the HTML content from the given URL.

        Parameters:
            url (str): The URL to fetch the HTML from.

        Returns:
            requests.Response: The HTTP response object containing
            the HTML content.
        """
        logger.debug("Attempting to fetch HTML content.")
        logger.debug('Attempting HTTP request with:')
        logger.debug(f'URL: {url}')
        logger.debug(f'timeout_policy: {self.timeout_policy}')
        logger.debug(f'headers: {self.headers}')
        logger.debug(f'retries: {self.retries}')
        try:
            response = self.session.get(
                url,
                headers=self.headers,
                timeout=self.timeout_policy
            )
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout as e:
            logger.error('Request timed out. Try increasing '
                         'the timeout policy. For instructions, '
                         'see pollscraper --help')
            raise e
        except requests.exceptions.HTTPError as e:
            logger.error(f'requests.exceptions.HTTPError: {e}')
            raise e
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching HTML: {e}')
            raise e

    def extract_html_table_data(self, table):
        """
        Extract table data from the HTML.

        Parameters:
            table (BeautifulSoup.Tag): The HTML table element.

        Returns:
            list: A list of lists containing the table data.
        """
        logger.debug("Attempting to extract HTML content.")
        table_data = []
        for row in table.find_all('tr'):
            row_data = [
                cell.get_text(strip=True) for cell in row
                    .find_all(['th', 'td'])
                ]
            table_data.append(row_data)
        return table_data

    def parse_html_bs4(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table')
        if not tables:
            logger.warning("No table found on the website.")
            raise ValueError('No tables found')
        n_tables = len(tables)
        if n_tables > 1:
            logger.warning('Unexpected URL format - '
                           f'{n_tables} tables found.'
                           'Only processing the first table.')
        table_data = self.extract_html_table_data(tables[0])
        return self.table_data_to_dataframe(table_data)

    def parse_html_table(self, html_content):
        """
        Parse the HTML content to extract tables.

        Parameters:
            html_content (str): The HTML content as a string.

        Returns:
            list or list of lists: A list of tables as DataFrames
            if found, otherwise a list of list of lists.
        """
        logger.debug("Attempting to parse HTML content.")
        try:
            return pd.read_html(html_content)[0]
        except ValueError as ve:
            logging\
                .warning(f'Pandas failed to read html content with error {ve}')
            logger.info('Falling back to BeautifulSoup.')
            return self.parse_html_bs4(html_content)
        except Exception as e:
            logger.error(f"Error extracting table data: {e}")
            raise e

    def extract_table_data(self, url):
        """
        Extract table data from the given URL.

        Parameters:
            url (str): The URL to fetch and extract data from.

        Returns:
            list or pandas.DataFrame: A list of lists if table
            data is found.
        """
        # OO library to ingest URL string formats (slightly overkill)
        url = URL(url)
        response = self.fetch_html_content(url)
        if url.suffix == '.html':
            table_data = self.parse_html_table(response.content)
        else:
            logger.warning(f'Error extracting data from source {url}')
            logger.warning('No protocol yet implemented for '
                           f'scraping {url.suffix} sources.')
            raise ValueError('Undefined URL format.')
        return table_data

    def table_data_to_dataframe(self, table_data):
        """
        Convert BeautifulSoup response table data into pandas.DataFrame.

        Parameters:
            table_data (list or pandas.DataFrame): The table data to process.

        Returns:
            pandas.DataFrame: The processed DataFrame.
        """
        logger.debug("Processing parsed data.")
        if isinstance(table_data, pd.DataFrame):
            return table_data
        if isinstance(table_data, list):
            processed_data = pd.DataFrame(
                    table_data[1:], columns=table_data[0]
                )
        else:
            raise TypeError("Unsupported data type for processing.")
        return processed_data

    def clean_data(self, table_df):
        """_summary_

        Parameters:
            table_df (pandas.DataFrame): pandas.DataFrame scraped from
                                         target URL
        Returns:
            pandas.DataFrame: Cleaned DataFrame
        """
        common_headers = list(self.common_header_mapping.keys())
        candidate_headers = sorted(
                list(set(table_df.columns)-set(common_headers))
            )
        expected_headers = common_headers + candidate_headers

        # Clean missing values
        missing_values = ["n/a", "na", "--", '**', '', 'NaN', '*']
        table_df.replace(missing_values, np.nan, inplace=True)

        # Remove remaining asterisks
        for c in expected_headers:
            table_df[c] = table_df[c].str.rstrip('*')

        # parse dates
        try:
            table_df['Date'] = pd.to_datetime(
                    table_df['Date'], errors='raise', format='%m/%d/%y'
                )
        except pd._libs.tslibs.parsing.DateParseError as e:
            logger.fatal('Date Time parsing error.')
            raise e

        # Date parsing check
        invalid_dates = table_df[table_df['Date'].isnull()]
        if not invalid_dates.empty:
            logger.warning(f"Invalid dates detected: {invalid_dates}")

        # Sort results by date
        table_df = table_df.sort_values(by='Date', ascending=False)

        # Cast polling count to integers.
        table_df['Sample'] = pd.to_numeric(table_df['Sample'],
                                           errors='coerce',
                                           downcast='integer')

        # Sample size validation
        invalid_samples = table_df[table_df['Sample'] < 10]
        if not invalid_samples.empty:
            logger.warning(f"Small sample sizes detected: {invalid_samples}")

        # Calculate and check polling fractions
        for c in candidate_headers:
            table_df[c] = table_df[c].str.rstrip('%').astype('float')/100
        table_df['combined_percentage'] = table_df[candidate_headers]\
            .sum(axis=1)

        for c in candidate_headers:
            table_df[c] = table_df[c]

        checksum = table_df[
                ~np.isclose(table_df['combined_percentage'], 1, atol=0.02)
            ].shape[0]
        if checksum > 0:
            logger.warning(f'{checksum} Row(s) with unbalanced vote-share')

        table_df = table_df[expected_headers]
        return table_df.rename(columns=self.common_header_mapping)


def main():
    url = 'https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html'
    dp = DataPipeline()
    table_df = dp.extract_table_data(url)
    processed_data = dp.clean_data(table_df)
    print(processed_data)


if __name__ == "__main__":
    main()
