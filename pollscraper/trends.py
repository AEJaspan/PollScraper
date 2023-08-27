import pandas as pd
# from pollscraper import logger
from datetime import datetime


class PollTrend:
    """
    Represents poll trends and provides methods to calculate trends.

    This class calculates average poll trends based on poll data.

    Attributes:
        None
    """

    @classmethod
    def calculate_trends(cls, poll_data):
        """
        Calculate poll trends based on poll data.

        Args:
            poll_data (PollData): Poll data containing poll information.

        Returns:
            pandas.DataFrame:
                DataFrame containing daily trends for each candidate.
        """
        poll_data = poll_data.sort_values(by='date')

        # Create a date range starting from
        # October 11th, 2023, to the last poll date
        start_date = datetime(2023, 10, 11)
        end_date = poll_data['date'].max()
        date_range = pd.date_range(start=start_date, end=end_date)

        # Initialize an empty DataFrame to store trends
        trends = pd.DataFrame({'date': date_range})

        # Calculate rolling average trends for each candidate
        for candidate in poll_data.columns[3:]:
            rolling_avg = poll_data[candidate]\
                .rolling(window=7, min_periods=1).mean()
            trends[candidate] = rolling_avg

        return trends
