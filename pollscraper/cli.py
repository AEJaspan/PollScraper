"""Console script for pollscraper."""
import sys
import click
import logging
from pollscraper.pollscraper import DataPipeline


@click.command()
@click.option('--url', default='https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html', prompt='Target URL.', help='Target URL containing polling data.')
@click.option('--results', default='data/data.csv', prompt='Output data path.', help='Location for scraped polling data to be stored.')
@click.option('--debug', default=logging.DEBUG, prompt='Logging Level.', help='Level of verbosity for debugging.')
def main(url, results, debug):
    try:
        dp = DataPipeline()
        table_data = dp.extract_table_data(url)
        processed_data = dp.process_data(table_data)
        dp.save_to_csv(processed_data, results)
        return 0
    except Exception as e:
        print(e)
        return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
