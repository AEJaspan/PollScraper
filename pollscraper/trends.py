import pandas as pd
import numpy as np
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
    def calculate_trends(cls, poll_data, n_sigma=5):
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
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        poll_data.set_index('date', inplace=True)
        # Initialize an empty DataFrame to store trends
        trends = pd.DataFrame({'date': date_range})
        outliers_avg = pd.DataFrame()
        outliers_poll = pd.DataFrame()

        # Calculate average on each day and calculate
        # rolling average trends for each candidate
        for candidate in poll_data.columns[3:]:
            resampled_candidates = poll_data[candidate].resample('D').mean()

            # Ensure there are no missing date stamps
            candidate_data = resampled_candidates.reindex(date_range)

            # Calculate 7 day rolling averages and standard deviations
            rolling_avg = candidate_data.rolling('7D').mean()
            rolling_std = candidate_data.rolling('7D').std()

            # Use standard deviations to check for outliers
            # Check against averaged poll data
            avg_outliers = check_for_outliers_in_poll_averages(
                candidate_data, rolling_avg, rolling_std, n_sigma)
            # Check against each individual poll
            individual_outliers = check_for_outliers_in_individual_polls(
                poll_data, candidate, rolling_avg, rolling_std, n_sigma)
            trends[candidate] = rolling_avg
            outliers_avg[candidate] = avg_outliers
            outliers_poll.join(individual_outliers, how='outer')

        logger.info('Rolling averages calculated.')
        return trends, outliers_avg, outliers_poll


def check_for_outliers_in_poll_averages(poll_averages, avg, sig, n_sigma):
    avg_outliers = poll_averages.loc[
        np.abs(poll_averages - avg) >= n_sigma * sig
    ]
    if not avg_outliers.empty:
        logger.warning(f'{avg_outliers.shape[0]} poll averages detected '
                       f'at > {n_sigma} sigma from the mean')
    return avg_outliers


def check_for_outliers_in_individual_polls(
            poll_data, candidate, avg, sig, n_sigma
        ):
    rolling = pd.DataFrame()
    rolling['sigma_band'] = sig
    rolling['rolling_avg'] = avg
    # Left join of the rolling variables to the individual polls
    check_individual_polls = poll_data[candidate].to_frame()\
        .join(rolling)

    individual_outliers = check_individual_polls.loc[
        np.abs(
                check_individual_polls[candidate] -
                check_individual_polls['rolling_avg']
            )
        >= n_sigma * check_individual_polls['sigma_band']
    ]
    if not individual_outliers.empty:
        logger.warning(f'{individual_outliers.shape[0]} individual polls '
                       f'detected at > {n_sigma} sigma from the mean')
    return individual_outliers[candidate]
