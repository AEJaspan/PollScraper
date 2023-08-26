"""Main module."""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from urlpath import URL


class DataPipeline:
    """
    DataPipeline class for processing and transforming data.

    This class provides methods to load data from a source,
    transform it, and save it to a destination.

    Attributes:
        source (str): The path to the source file.
        destination (str): The path to the destination file.
        logger (logging.Logger): Logger instance for logging messages.
    """

    def __init__(self, LOGGING_LEVEL=logging.DEBUG):
        """
        Initialize the DataPipeline object.
        """
        self.logger = logging.getLogger(__name__)
        # Set the log level and other configurations for the logger
        self.logger.setLevel(LOGGING_LEVEL)
        formatter = logging\
            .Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.logger.debug("Data Pipeline Initialised.")

    def fetch_html_content(self, url):
        """
        Fetch the HTML content from the given URL.

        Parameters:
            url (str): The URL to fetch the HTML from.

        Returns:
            requests.Response: The HTTP response object containing
            the HTML content.
        """
        self.logger.debug("Attempting to fetch HTML content.")
        try:
            headers = {'Accept-Encoding': 'identity'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            # Raise exception for 4xx and 5xx status codes
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Error fetching HTML: {e}')
            raise

    def extract_html_table_data(self, table):
        """
        Extract table data from the HTML.

        Parameters:
            table (BeautifulSoup.Tag): The HTML table element.

        Returns:
            list: A list of lists containing the table data.
        """
        self.logger.debug("Attempting to extract HTML content.")
        table_data = []
        for row in table.find_all('tr'):
            row_data = [
                cell.get_text(strip=True) for cell in row
                    .find_all(['th', 'td'])
                ]
            table_data.append(row_data)
        return table_data

    def parse_html_table(self, html_content):
        """
        Parse the HTML content to extract tables.

        Parameters:
            html_content (str): The HTML content as a string.

        Returns:
            list or list of lists: A list of tables as DataFrames
            if found, otherwise a list of list of lists.
        """
        self.logger.debug("Attempting to parse HTML content.")
        try:
            raise ValueError
            return pd.read_html(html_content)
        except ValueError as ve:
            self.logger\
                .warning(f'Pandas failed to read html content with error {ve}')
            self.logger.info('Falling back to bs4.')
            soup = BeautifulSoup(html_content, 'html.parser')
            tables = soup.find_all('table')
            if not tables:
                self.logger.warning("No table found on the website.")
                raise ValueError('No tables found')
            table_list = []
            for table in tables:
                table_list.append(self.extract_html_table_data(table))
            return table_list
        except Exception as e:
            self.logger.error(f"Error extracting table data: {e}")
            raise

    def parse_xml_table(self, xml_content):
        """
        Parse the XML content to extract data.

        Parameters:
            xml_content (str): The XML content as a string.

        Returns:
            list of dict: A list of dictionaries containing the extracted data.
        """
        self.logger.debug("Attempting to parse XML content.")
        try:
            if 'read_xml' not in pd.__dict__:
                raise AttributeError(
                    f"""Read XML method only available in pandas>=1.3.0.
                    (Python>=3.7.1) Current pandas=={pd.__version__}.""")
            return pd.read_xml(xml_content)
        except (ValueError, AttributeError) as e:
            self.logger\
                .warning(f'Pandas failed to read xml content with error {e}')
            self.logger.info('Falling back to bs4.')
            soup = BeautifulSoup(xml_content, 'xml')
            data_elements = soup.find_all('Keyword')

            data_list = []
            for element in data_elements:
                data = {
                    'Term': element.find('Term').get_text(),
                    'Vocabulary': element.find('Vocabulary').get_text(),
                    'Definition': element.find('Definition').get_text()
                }
                data_list.append(data)
            return pd.DataFrame(data_list)
        except Exception as e:
            self.logger.error(f"Error extracting data from XML: {e}")
            return None

    def scrape_csv(self, url):
        """
        Scrape data from a CSV file.

        Parameters:
            url (str): The URL of the CSV file.

        Returns:
            pandas.DataFrame: The DataFrame containing the CSV data.
        """
        self.logger.debug("Attempting to parse CSV content.")
        return pd.read_csv(url)

    def extract_table_data(self, url):
        """
        Extract table data from the given URL.

        Parameters:
            url (str): The URL to fetch and extract data from.

        Returns:
            list or pandas.DataFrame: A list of lists if table
            data is found, or DataFrame if CSV data is found.
        """
        self.logger.debug(f"Attempting to access content from {url}.")
        url = URL(url)
        if url.suffix == '.csv':
            return self.scrape_csv(url)
        response = self.fetch_html_content(url)
        if url.suffix == '.html':
            table_data = self.parse_html_table(response.content)[0]
        elif url.suffix == '.xml':
            table_data = self.parse_xml_table(response.content)
        else:
            raise Exception('Undefined table format.')
        return table_data

    def process_data(self, table_data):
        """
        Process the table data.

        Parameters:
            table_data (list or pandas.DataFrame): The table data to process.

        Returns:
            pandas.DataFrame: The processed DataFrame.
        """
        self.logger.debug("Processing parsed data.")
        if isinstance(table_data, list):
            # Process list of lists
            processed_data = pd.DataFrame(
                    table_data[1:], columns=table_data[0]
                )
        elif isinstance(table_data, pd.DataFrame):
            # Process DataFrame
            processed_data = table_data
        else:
            raise TypeError("Unsupported data type for processing.")
        return processed_data

    def save_to_csv(self, data, file_path):
        """
        Save data to the destination file.

        Args:
            data (list): The data to be saved.

        Returns:
            None
        """
        self.logger.debug(f"Saving parsed data to {file_path}.")
        try:
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            self.logger.info(f"Data saved to {file_path}")
        except Exception as e:
            logging.error(f"Error saving data to CSV: {e}")
            raise


def main():
    url = 'https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html'
    file_path = 'data/data.csv'
    dp = DataPipeline()
    table_data = dp.extract_table_data(url)
    processed_data = dp.process_data(table_data)
    dp.save_to_csv(processed_data, file_path)


if __name__ == "__main__":
    main()
