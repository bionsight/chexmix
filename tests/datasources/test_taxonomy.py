from unittest.mock import Mock

from chexmix.data import taxonomy as taxonomy_data
from chexmix.datasources import taxonomy


def test_load_taxonomy(taxonomy_dmp_mock):
    taxonomy_data.load_taxdump = Mock(return_value=taxonomy_dmp_mock)
    taxonomy_table = taxonomy.load_taxonomy()
    assert (taxonomy_table['TAXO:33154']['level'] == 3) and (taxonomy_table['TAXO:131567']['level'] == 1)
