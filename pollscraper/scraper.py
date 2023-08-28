"""Main module."""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import logging
from urlpath import URL
from pollscraper import logger


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

    def __init__(self):
        """
        Initialize the DataPipeline object.
        """
        self.common_header_mapping = {
            'Date': 'date',
            'Pollster': 'pollster',
            'Sample': 'n'
        }
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
        try:
            headers = {'Accept-Encoding': 'identity'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            # Raise exception for 4xx and 5xx status codes
            return response
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
        logger.debug(f"Attempting to access content from {url}.")
        url = URL(url)
        response = self.fetch_html_content(url)
        if url.suffix == '.html':
            table_data = self.parse_html_table(response.content)
        else:
            raise Exception('Undefined URL format.')
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
                    table_df['Date'], errors='coerce',
                )
        except pd._libs.tslibs.parsing.DateParseError as e:
            logger.fatal('Date Time parsing error.')
            raise e

        # Date parsing check
        invalid_dates = table_df[table_df['Date'].isnull()]
        if not invalid_dates.empty:
            logger.warning(f"Invalid dates detected: {invalid_dates}")

        # Cast polling count to numeric.
        table_df['Sample'] = pd.to_numeric(table_df['Sample'], errors='coerce')

        # Sample size validation
        invalid_samples = table_df[table_df['Sample'] < 10]
        if not invalid_samples.empty:
            logger.warning(f"Small sample sizes detected: {invalid_samples}")

        # Calculate and check polling fractions
        for c in candidate_headers:
            table_df[c] = table_df[c].str.rstrip('%').astype('float')/100
        table_df['combined_percentage'] = table_df[candidate_headers]\
            .sum(axis=1)

        checksum = table_df[
                ~np.isclose(table_df['combined_percentage'], 1, atol=0.02)
            ].shape[0]
        if checksum > 0:
            logger.warning(f'{checksum} Row(s) with unbalanced vote-share')

        table_df = table_df[expected_headers]
        return table_df.rename(columns=self.common_header_mapping)


def main():
    from pollscraper.__init__ import update_log_level
    update_log_level(10)
    url = 'https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html'
    dp = DataPipeline()
    table_df = dp.extract_table_data(url)
    processed_data = dp.clean_data(table_df)
    print(processed_data)


if __name__ == "__main__":
    main()
