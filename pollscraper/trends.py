import pandas as pd
from pollscraper import logger
from datetime import datetime
from pandas.api.types import is_datetime64_any_dtype as is_datetime


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
        if not is_datetime(poll_data['date']):
            raise ValueError('Preprocessing step has been missed. '
                             'Date column incorrectly formatted')
        poll_data = poll_data.sort_values(by='date')

        # Create a date range starting from
        # October 11th, 2023, to the last poll date
        start_date = datetime(2023, 10, 11)
        end_date = poll_data['date'].max()
        date_range = pd.date_range(start=start_date, end=end_date)
        poll_data.set_index('date', inplace=True)
        # Initialize an empty DataFrame to store trends
        trends = pd.DataFrame({'date': date_range})

        # Calculate average on each day and calculate
        # rolling average trends for each candidate
        for candidate in poll_data.columns[3:]:
            rolling_avg = poll_data[candidate].groupby('date').mean()\
                .rolling('7D').mean()
            trends[candidate] = rolling_avg
        logger.info('Rolling averages calculated.')
        return trends
