# first party
from delphi.epidata.acquisition.covid_hosp.common.network import Network as BaseNetwork


class Network(BaseNetwork):

  DATASET_ID = '823dd0e-c8c4-4206-953e-c6d2f451d6ed'

  def fetch_metadata(*args, **kwags):
    """Download and return metadata.

    See `fetch_metadata_for_dataset`.
    """

    return Network.fetch_metadata_for_dataset(
        *args, **kwags, dataset_id=Network.DATASET_ID)
