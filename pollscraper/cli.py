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
def main(url, results_dir, quiet):
    try:
        filepath = f'{results_dir}'
        if quiet:
            logging.getLogger("urllib3").setLevel(logging.WARNING)
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.DEBUG)
        logger.debug(f'Info level set to {quiet}')
        dp = DataPipeline()
        logger.info('Extracting data from URL.')
        table_df = dp.extract_table_data(url)
        logger.info('Cleaning poll data.')
        processed_data = dp.clean_data(table_df)
        logger.info(f'Saving polling data to {filepath}/polls.csv')
        processed_data.to_csv(f'{filepath}/polls.csv')
        logger.info('Calculating trends.')
        trends, _, _ = PollTrend.calculate_trends(processed_data, n_sigma=5)
        logger.info(f'Saving trend data to {filepath}/trends.csv')
        trends.to_csv(f'{filepath}/trends.csv')
        logger.info('Operation completed sucessfully.')
        return 0
    except Exception as e:
        logger.error(e)
        return 0


if __name__ == "__main__":
    sys.exit(main())
