import pytest
from twitter_bot import text_generator

# Check that when there is nothing to be published, nothing is twitted.
def test_text_generator():
    assert text_generator({'Temperature': None, 'Extreme': False, 'Precipitation': None}) == None
