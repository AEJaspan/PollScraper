from click.testing import CliRunner
from pollscraper import cli
from pathlib import Path
from root import ROOT_DIR
from datetime import date


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
