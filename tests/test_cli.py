from click.testing import CliRunner
import pandas as pd
from pollscraper import cli
from pathlib import Path
from root import ROOT_DIR
from datetime import date

from pandas.api.types import is_numeric_dtype as is_numeric


def test_command_line_interface(get_target_url):
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    url = get_target_url
    output = 'data/'
    commands = f'--quiet --url {url} --results_dir {ROOT_DIR}/{output}'
    result = runner.invoke(cli.main, commands)
    assert result.exit_code == 0
    polls = Path(f"{ROOT_DIR}/{output}/polls.csv")
    assert polls.is_file()
    trends = Path(f"{ROOT_DIR}/{output}/trends.csv")
    assert trends.is_file()
    assert date.today() == date.fromtimestamp(polls.stat().st_mtime)
    assert date.today() == date.fromtimestamp(trends.stat().st_mtime)
    polls_df = pd.read_csv(polls, index_col=0)
    trends_df = pd.read_csv(trends, index_col=0)
    polls_df['date'] = pd.to_datetime(polls_df['date'], errors='raise')
    trends_df['date'] = pd.to_datetime(trends_df['date'], errors='raise')
    assert all(is_numeric(trends_df[col]) for col in trends_df.columns[1:])
    assert all(is_numeric(polls_df[col]) for col in polls_df.columns[3:])
