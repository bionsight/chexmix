import pytest

from chexmix.datasources import taxonomy
from chexmix.table import Taxonomy


@pytest.fixture
def a_taxonomy(monkeypatch, taxonomy_table):
    def taxonomy_table_mock():
        return taxonomy_table
    monkeypatch.setattr(taxonomy, 'load_taxonomy', taxonomy_table_mock)
    return Taxonomy('TAXO:9606', {'APPERAED_IN': ['ARTI:33992036']})


def test_taxonomy_table(a_taxonomy):
    assert a_taxonomy.taxonomy_table() == {
        'TAXO:63221': {
            'family': 'Hominidae',
            'genus': 'Homo',
            'hierarchy': {'_INCLUDES': ['TAXO:9606']},
            'id': 'TAXO:63221',
            'level': 68,
            'lineage': ['TAXO:9605', 'TAXO:9606'],
            'name': 'Homo sapiens neanderthalensis',
            'rank': 'subspecies',
            'raw_id': 63221,
            'type': 'Taxonomy'
        },
        'TAXO:9605': {
            'family': 'Hominidae',
            'genus': '',
            'hierarchy': {'INCLUDES': ['TAXO:9606']},
            'id': 'TAXO:9605',
            'level': 48,
            'lineage': [],
            'name': 'Homo',
            'rank': 'genus',
            'raw_id': 9605,
            'type': 'Taxonomy'
        },
        'TAXO:9606': {
            'family': 'Hominidae',
            'genus': 'Homo',
            'hierarchy': {'INCLUDES': ['TAXO:63221'], '_INCLUDES': ['TAXO:9605']},
            'id': 'TAXO:9606',
            'level': 64,
            'lineage': ['TAXO:9605'],
            'name': 'Homo sapiens',
            'rank': 'species',
            'raw_id': 9606,
            'type': 'Taxonomy'
        }
    }


def test_raw_id(a_taxonomy):
    assert a_taxonomy.raw_id == 9606


def test_name(a_taxonomy):
    assert a_taxonomy.name == 'Homo sapiens'


def test_rank(a_taxonomy):
    assert a_taxonomy.rank == 'species'


def test_family(a_taxonomy):
    assert a_taxonomy.family == 'Hominidae'


def test_genus(a_taxonomy):
    assert a_taxonomy.genus == 'Homo'


def test_level(a_taxonomy):
    assert a_taxonomy.level == 64


def test_lineage(a_taxonomy):
    assert a_taxonomy.lineage == ['TAXO:9605']


def test_relationship(a_taxonomy):
    assert a_taxonomy.relationship == {
        'APPERAED_IN': ['ARTI:33992036'], 'INCLUDES': ['TAXO:63221'], '_INCLUDES': ['TAXO:9605']
    }
