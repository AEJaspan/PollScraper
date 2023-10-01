import pandas as pd
import numpy as np
from pollscraper import logger
from datetime import datetime
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from sklearn.preprocessing import MinMaxScaler

from pandas.core.window.rolling import _flex_binary_moment, _Rolling_and_Expanding
def weighted_mean(self, weights, **kwargs):
    weights = self._shallow_copy(weights)
    window = self._get_window(weights)

    def _get_weighted_mean(X, Y):
        X = X.astype('float64')
        Y = Y.astype('float64')
        sum_f = lambda x: x.rolling(window, self.min_periods, center=self.center).sum(**kwargs)
        return sum_f(X * Y) / sum_f(Y)

    return _flex_binary_moment(self._selected_obj, weights._selected_obj,
                               _get_weighted_mean, pairwise=True)


def weighted_std(self, weights, **kwargs):
    weights = self._shallow_copy(weights)
    window = self._get_window(weights)

    def _get_weighted_std(X, Y):
        X = X.astype('float64')
        Y = Y.astype('float64')
        sum_f = lambda x: x.rolling(window, self.min_periods, center=self.center).sum(**kwargs)
        sum_weights = sum_f(Y)
        W_non_zero = Y>=0
        wav = sum_f(X * Y) / sum_weights
        numerator = sum_f(Y*X-wav)**2
        denom = sum_weights * (W_non_zero-1) / W_non_zero
        return numerator / denom

    return _flex_binary_moment(self._selected_obj, weights._selected_obj,
                               _get_weighted_std, pairwise=True)

_Rolling_and_Expanding.weighted_mean = weighted_mean
_Rolling_and_Expanding.weighted_std = weighted_std

def modality_factor(sample_weights, modality_col):
    map={'Online': 0.9, 'IVR': 0.95, 'Live caller': 1.}
    if type(modality_col) == type(None):
        return
    assert type(modality_col) == pd.Series
    sample_weights*=modality_col.map(map).fillna(1)

def sponsor_factor(sample_weights, sponsor_col):
    if type(sponsor_col) == type(None):
        return
    assert type(sponsor_col) == pd.Series
    # sample_weights*=population_col.map(map).fillna(1)

def population_factor(sample_weights, population_col):
    map={'Adults': 0.9, 'RV': 0.95, 'LV': 1.}
    if type(population_col) == type(None):
        return
    assert type(population_col) == pd.Series
    sample_weights*=population_col.map(map).fillna(1)

def pollster_factor(sample_weights, pollster_col):
    map={'Dataland Daily': 1., 'No Province Left Behind': 1., 'Progressive Polling': 1.,
     'Cobolite Coalition Calling': 1., 'Big Dataland Surveys': 1.,
     'Synapse Strategies': 1., 'Metaflux University': 1.,
     'Conference Board of Dataland': 1., 'Dataland Register-Gazette': 1.,
     'Proudly Paid For Polling': 1., 'Electropolis Elects': 1.}
    if type(pollster_col) == type(None):
        return
    assert type(pollster_col) == pd.Series
    sample_weights*=pollster_col.map(map).fillna(1)

def weighting_scheme_538(samples,
                         modality_col=None,
                         sponsor_col=None,
                         population_col=None,
                         pollster_col=None):
    avg_sample_size = samples.mean()
    sample_weights = np.sqrt(samples/avg_sample_size)
    modality_factor(sample_weights, modality_col)
    sponsor_factor(sample_weights, sponsor_col)
    population_factor(sample_weights, population_col)
    pollster_factor(sample_weights, pollster_col)
    return sample_weights

def weighting_scheme_min_max(samples,
                         modality_col=None,
                         sponsor_col=None,
                         population_col=None,
                         pollster_col=None):
    sample_weights = MinMaxScaler().fit_transform(
                np.array(samples).reshape(-1,1)
            )
    modality_factor(sample_weights, modality_col)
    sponsor_factor(sample_weights, sponsor_col)
    population_factor(sample_weights, population_col)
    pollster_factor(sample_weights, pollster_col)
    return sample_weights

# def weighted_average(group):
#     return group.apply(lambda x: np.average(x.wt, weights=x.value))


def wavg(group):
    d = group.iloc[:,0]
    w = group.iloc[:,1]
    return (d * w).sum() / w.sum()

class PollTrend:
    """
    Represents poll trends and provides methods to calculate trends.

    This class calculates average poll trends based on poll data.

    Attributes:
        None
    """

    @classmethod
    def calculate_trends(cls, poll_data, n_sigma=5, weights_col=None): #modality_col='', sponsor_col='', population_col=''):
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
        poll_data = poll_data.sort_values(by='date', ascending=False)
        if type(weights_col) == type(None):
            weights_col = 'weights'
            poll_data[weights_col] = 1.
        
        # poll_metadata = [c for c in [modality_col, sponsor_col, population_col] if c!='']
        # candidate_cols = poll_data.columns[2:]
        reserved_cols = ['pollster', 'n', 'date', weights_col]#+[poll_metadata]
        candidate_cols = sorted(
            [c for c in poll_data.columns if c not in reserved_cols]
        )
        # Create a date range starting from
        # October 11th, 2023, to the last poll date
        start_date = poll_data['date'].min() # datetime(2023, 10, 11)
        end_date = poll_data['date'].max()
        date_range = pd.date_range(
                start=start_date, end=end_date, freq='D'
            )[::-1]
        poll_data.set_index('date', inplace=True)
        # poll_data['weights'] = weighting_scheme_min_max(
        #         poll_data['n']
        #     )
        # poll_data['weights'] = weighting_scheme_538(
        #         poll_data['n'], **{k:poll_data[k] for k in poll_metadata}
        #     )
        # Initialize an empty DataFrame to store trends
        trends = pd.DataFrame(index=date_range)
        outliers_avg = pd.DataFrame()
        outliers_poll = pd.DataFrame()

        # Calculate average on each day and calculate
        # rolling average trends for each candidate
        for candidate in candidate_cols:
            weighted_candidate = poll_data[[candidate, weights_col]] # * poll_data['weights']
            # resampled_candidates = weighted_candidate.resample('D').mean() #resampled_candidates = weighted_candidate).mean()
            resampled_candidates = weighted_candidate.groupby(
                    pd.Grouper(freq='D')
                ).apply(wavg)
            problems = resampled_candidates[
                    (resampled_candidates > 1.001) | (resampled_candidates < .99)
                ]
            if problems.shape[0] > .05 * resampled_candidates.shape[0]:
                logger.warning('Imbalance after re-weighting.')
            # resampled_candidates = weighted_candidate.resample('D').agg({candidate:'mean', 'weights':'mean'})
            # Ensure there are no missing date stamps
            candidate_data = resampled_candidates.reindex(date_range)

            # Invert for left aligned windows, then restore
            rolling_avg = candidate_data[::-1].rolling('7D').mean()[::-1]
            rolling_std = candidate_data[::-1].rolling('7D').std()[::-1]
            # rolling_avg = candidate_data[candidate][::-1].rolling('7D').weighted_mean(weights=candidate_data['weights'])[::-1]
            # rolling_std = candidate_data[candidate][::-1].rolling('7D').weighted_std(weights=candidate_data['weights'])[::-1]
            # Use standard deviations to check for outliers
            # Check against averaged poll data
            avg_outliers = check_for_outliers_in_poll_averages(
                candidate_data, rolling_avg, rolling_std, n_sigma, candidate
            )
            # Check against each individual poll
            individual_outliers = check_for_outliers_in_individual_polls(
                poll_data, candidate, rolling_avg, rolling_std, n_sigma
            )
            trends[candidate] = rolling_avg
            outliers_avg[candidate] = avg_outliers
            outliers_poll.join(individual_outliers, how='outer')
        trends.index.name = 'date'
        # trends.set_index('date',inplace=True)
        # Sort columns so that they are in descending order from latest poll
        trends.sort_values(
                trends.first_valid_index(),
                axis=1, inplace=True,
                ascending=False
            )
        trends.reset_index(inplace=True)
        logger.info('Rolling averages calculated.')
        return trends, outliers_avg, outliers_poll


def check_for_outliers_in_poll_averages(
            poll_averages, avg, sig, n_sigma, candidate
        ):
    avg_outliers = poll_averages.loc[
        np.abs(poll_averages - avg) >= n_sigma * sig
    ]
    if not avg_outliers.empty:
        logger.warning(f'Checking averaged polls for candidate {candidate}.')
        logger.warning(f'Found {avg_outliers.shape[0]} poll averages detected '
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
        logger.warning(f'Checking individual polls for candidate {candidate}.')
        logger.warning(f'Found {individual_outliers.shape[0]} individual '
                       f'polls detected at > {n_sigma} sigma from the mean')
    return individual_outliers[candidate]
