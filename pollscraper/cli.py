"""Console script for pollscraper."""
import sys
import click
import logging
from pollscraper.scraper import DataPipeline
from pollscraper.trends import PollTrend
from pollscraper import logger
from pollscraper.__init__ import update_log_level
from root import ROOT_DIR


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
@click.option('--debug',
              default=logging.DEBUG,
              prompt='Logging Level.',
              help='Level of verbosity for debugging.')
def main(url, results_dir, debug):
    try:
        filepath = f'{ROOT_DIR}/{results_dir}'
        update_log_level(debug)
        logger.debug(f'Info level set to {debug}')
        dp = DataPipeline()
        logger.info('Extracting data from URL.')
        table_df = dp.extract_table_data(url)
        logger.info('Cleaning poll data.')
        processed_data = dp.clean_data(table_df)
        logger.info(f'Saving polling data to {filepath}/polls.csv')
        processed_data.to_csv(f'{filepath}/polls.csv', index=False)
        logger.info('Calculating trends.')
        trends = PollTrend.calculate_trends(processed_data)
        logger.info(f'Saving trend data to {filepath}/trends.csv')
        trends.to_csv(f'{filepath}/trends.csv', index=False)

        return 0
    except Exception as e:
        print(e)
        return 0


if __name__ == "__main__":
    sys.exit(main())
