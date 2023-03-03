import pytest

from chexmix.table import Publication


@pytest.fixture
def publication():
    return Publication(
        'ARTI:3018002', {'_APPEARED_IN': []},
        'Purified HDL-apolipoproteins, A-I and C-III, substitute for HDL in '
        'promoting the growth of SV40-transformed REF52 cells in serum-free medium.',
        'J Cell Physiol', {'pubmed': [], 'medline': [], 'entrez': ''}, '3')


def test_raw_id(publication):
    assert publication.raw_id == '3018002'


def test_name(publication):
    assert publication.name == 'Purified HDL-apolipoproteins, A-I and C-III, substitute for HDL in promoting ' \
                               'the growth of SV40-transformed REF52 cells in serum-free medium.', 'J Cell Physiol'


def test_uid_from():
    assert Publication.uid_from('3018002') == 'ARTI:3018002'


def test_normalize():
    normed_table = Publication.normalize([{
        'Id': '3018002', 'Source': 'J Cell Physiol', 'Issue': '3',
        'Title': 'Purified HDL-apolipoproteins, A-I and C-III, substitute for HDL in promoting the growth of '
                 'SV40-transformed REF52 cells in serum-free medium.',
        'History': {'pubmed': ['1986/09/01 00:00'], 'medline': ['1986/09/01 00:01'], 'entrez': '1986/09/01 00:00'}}])

    assert list(normed_table.keys()) == ['ARTI:3018002']
    assert list(normed_table.values())[0].id == 'ARTI:3018002'
    assert list(normed_table.values())[0].raw_id == '3018002'
    assert list(normed_table.values())[0].name == 'Purified HDL-apolipoproteins, A-I and C-III, substitute for HDL' \
                                                  ' in promoting the growth of SV40-transformed REF52 cells ' \
                                                  'in serum-free medium.'
    assert list(normed_table.values())[0].extra_relationship == {'_APPEARED_IN': []}
    assert list(normed_table.values())[0].source == 'J Cell Physiol'
    assert list(normed_table.values())[0].history == {'pubmed': ['1986/09/01 00:00'], 'medline': ['1986/09/01 00:01'],
                                                      'entrez': '1986/09/01 00:00'}
    assert list(normed_table.values())[0].issue == '3'
