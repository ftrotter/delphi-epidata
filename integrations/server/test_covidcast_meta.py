"""Integration tests for the `covidcast_meta` endpoint."""

# standard library
import unittest

# third party
import mysql.connector
import requests


# use the local instance of the Epidata API
BASE_URL = 'http://delphi_web_epidata/epidata/api.php'


class CovidcastMetaTests(unittest.TestCase):
  """Tests the `covidcast_meta` endpoint."""

  def setUp(self):
    """Perform per-test setup."""

    # connect to the `epidata` database and clear the `covidcast` table
    cnx = mysql.connector.connect(
        user='user',
        password='pass',
        host='delphi_database_epidata',
        database='epidata')
    cur = cnx.cursor()
    cur.execute('truncate table covidcast')
    cnx.commit()
    cur.close()

    # make connection and cursor available to test cases
    self.cnx = cnx
    self.cur = cnx.cursor()

  def tearDown(self):
    """Perform per-test teardown."""
    self.cur.close()
    self.cnx.close()

  def test_round_trip(self):
    """Make a simple round-trip with some sample data."""

    # insert dummy data and accumulate expected results (in sort order)
    template = '''
      insert into covidcast values
        (0, "%s", "%s", "%s", "%s", %d, "%s", %d, 0, 0, 0)
    '''
    expected = []
    for src in ('src1', 'src2'):
      for sig in ('sig1', 'sig2'):
        for tt in ('day', 'week'):
          for gt in ('hrr', 'msa'):
            expected.append({
              'data_source': src,
              'signal': sig,
              'time_type': tt,
              'geo_type': gt,
              'min_time': 1,
              'max_time': 2,
              'num_locations': 2,
              'min_value': 10,
              'max_value': 20,
              'mean_value': 15,
              'stdev_value': 5,
            })
            for tv in (1, 2):
              for gv, v in zip(('geo1', 'geo2'), (10, 20)):
                self.cur.execute(template % (src, sig, tt, gt, tv, gv, v))
    self.cnx.commit()

    # make the request
    response = requests.get(BASE_URL, params={'source': 'covidcast_meta'})
    response.raise_for_status()
    response = response.json()

    # assert that the right data came back
    self.assertEqual(response, {
      'result': 1,
      'epidata': expected,
      'message': 'success',
    })
