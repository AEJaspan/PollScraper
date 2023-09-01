"""Console script for pollscraper."""
import sys
import click
import logging
from pollscraper.scraper import DataPipeline
from pollscraper.trends import PollTrend
from pollscraper import logger


URL = 'https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html'


@click.command()
@click.option('--url',
              default=URL,
              prompt='Target URL.',
              help='Target URL containing polling data.')
@click.option('--results_dir',
              default='data/',
              prompt='Output data path.',
              help='Location for scraped polling data to be stored.')
@click.option('--quiet', default=False, is_flag=True,
              help='Reduce streamed logging output. '
                   '(This does not affect output in the log file)')
@click.option('--n_places', default=4, help="Set floating point precision "
              "stored in the output .csv files.")
@click.option('--connect_timeout', default=3.05, help="The connect timeout is "
              "the number of seconds Requests will wait for your "
              "client to establish a connection to a remote machine "
              "(corresponding to the connect()) call on the socket. "
              "It's a good practice to set connect timeouts to slightly "
              "larger than a multiple of 3, which is the default TCP "
              "packet retransmission window.")
@click.option('--read_timeout', default=30, help='Once your client has '
              'connected to the server and sent the HTTP request, '
              'the read timeout is the number of seconds the client '
              "will wait for the server to send a response.")
@click.option('--http_n_retries', default=5, help="Sets number of "
              "automatic retries to connect to target HTML after failed "
              "connection")
def main(url, results_dir, quiet, connect_timeout,
         read_timeout, http_n_retries, n_places) -> None:
    try:
        filepath = f'{results_dir}'
        if quiet:
            logging.getLogger("urllib3").setLevel(logging.WARNING)
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.DEBUG)
        logger.info('Running PollScraper Pipeline!')
        logger.debug('Logging set to logging.DEBUG '
                     'Reduce logging output with flag: '
                     '--quiet')
        dp = DataPipeline(connect_timeout, read_timeout, http_n_retries)
        logger.debug('Extracting data from URL.')
        table_df = dp.extract_table_data(url)
        logger.debug('Cleaning poll data.')
        processed_data = dp.clean_data(table_df)
        logger.info(f'Saving polling data to {filepath}/polls.csv')
        # Save to n decimal places
        processed_data.to_csv(f'{filepath}/polls.csv',
                              float_format=f'%.{n_places}f')
        logger.debug('Calculating trends.')
        trends, _, _ = PollTrend.calculate_trends(processed_data, n_sigma=5)
        logger.info(f'Saving trend data to {filepath}/trends.csv')
        # Save to n decimal places
        trends.to_csv(f'{filepath}/trends.csv',
                      float_format=f'%.{n_places}f')
        logger.info('Operation completed successfully.')
        return 0
    except Exception as e:
        logger.error(e)
        return 0


if __name__ == "__main__":
    sys.exit(main())
