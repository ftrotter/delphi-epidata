"""Utility functions only used in tests.

This code is not used in production.

The functions in this file are used by both unit and integration tests.
However, unit tests can't import code that lives in integration tests, and vice
versa. As a result, common test code has to live under the top-level `/src`
dir, hence the existence of this file.
"""

# standard library
import json
from pathlib import Path
from unittest.mock import Mock

# third party
import pandas


class TestUtils:

  # path to `covid_hosp` test data, relative to the top of the repo
  PATH_TO_TESTDATA = 'testdata/acquisition/covid_hosp'

  def __init__(self, abs_path_to_caller):
    # navigate to the root of the delphi-epidata repo
    dataset_name = None
    current_path = Path(abs_path_to_caller)
    while not (current_path / 'testdata').exists():

      # bail if we made it all the way to root
      if not current_path.name:
        raise Exception('unable to determine path to delphi-epidata repo')

      # looking for a path like .../acquisition/covid_hosp/<dataset>
      if current_path.parent.name == 'covid_hosp':
        dataset_name = current_path.name

      # move up one level
      current_path = current_path.parent

    # the loop above stops at the top of the repo
    path_to_repo = current_path

    if not dataset_name:
      raise Exception('unable to determine name of dataset under test')

    # path dataset-specific test data, relative to the root of the repo
    self.data_dir = (
        path_to_repo / TestUtils.PATH_TO_TESTDATA / dataset_name
    ).resolve()

  def load_sample_metadata(self):
    with open(self.data_dir / 'metadata.json', 'rb') as f:
      return json.loads(f.read().decode('utf-8'))

  def load_sample_dataset(self):
    return pandas.read_csv(self.data_dir / 'dataset.csv', dtype=str)

  def load_sample_revisions(self):
    """Pretend to serve pages from the HHS revisions site.

    These are scraped by state_daily to ensure we capture all files, not just the
    most recent in each batch uploaded by HHS.
    """
    for filename in [f'revision{x}.html' for x in
                     ['s', '_0130', '_0129', '_0128', '_0127']]:
      with open(self.data_dir / filename, 'rb') as f:
        yield Mock(content=f.read().decode('utf-8'))
