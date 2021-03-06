from fake_web_events import load_config
import pytest


config = load_config()


class SumNotOneException(Exception):
    """
    Custom exception for error reporting.
    """
    def __init__(self, key, key_sum, message="Sum of probabilities is not equal to 1"):
        self.key = key
        self.key_sum = key_sum
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}.\n{self.key} == {self.key_sum}. Make sure it is equal 1.'


def _sum_pages():
    for page in config['pages']:
        yield page, sum(config['pages'][page].values())


class TestConfig:

    @pytest.mark.parametrize("page, page_sum", _sum_pages())
    def test_sum_pages(self, page, page_sum):
        if page_sum != 1:
            raise SumNotOneException(page, page_sum)

    @pytest.mark.parametrize("parameter", ['visits_per_hour', 'operating_systems', 'marketing_sources', 'ads',
                                           'campaigns', 'marketing_mediums', 'browsers', 'landing_pages'])
    def test_sum_others(self, parameter):
        sum_parameter = sum(config[parameter].values())
        if sum_parameter != 1:
            raise SumNotOneException(parameter, sum_parameter)
