from chexmix.datasources import mesh, taxonomy
from chexmix.table.utils import search_by_keyword
import chexmix.datasources.entrez as ez
import chexmix.datasources.pubtator as pt


def test_search_by_keyword(monkeypatch, mesh_table, taxonomy_table):
    def pubmed_mock(keyword):
        return [{'Id': '2', 'Title': 'test title', 'Source': 'bion', 'History': {
            'pubmed': ['1980/03/01'], 'medline': ['1980/03/01'], 'entrez': '1980/03/01'}, 'Issue': '1'}]

    def pubtator_mock(pmids):
        return [{
            'id': '2',
            'passages': [{
                'annotations': [{
                    'id': '10', 'infons': {'identifier': 'MESH:D058729', 'type': 'Chemical'},
                    'text': 'isoleucine', 'locations': [{'offset': 156, 'length': 19}]}, {
                    'id': '11', 'infons': {'identifier': 'MESH:C565928', 'type': 'Disease'},
                    'text': 'Hydroxyprolinemia', 'locations': [{'offset': 220, 'length': 21}]}, {
                    'id': '12', 'infons': {'identifier': '58510', 'type': 'Gene'},
                    'text': 'HYPDH', 'locations': [{'offset': 246, 'length': 11}]}, {
                    'id': '13', 'infons': {'identifier': '9606', 'type': 'Species'},
                    'text': 'rats', 'locations': [{'offset': 297, 'length': 12}]}]}],
            'pmid': 2, 'year': 1987}]

    def mesh_mock():
        return mesh_table

    def taxonomy_mock():
        return taxonomy_table

    monkeypatch.setattr(ez, 'search_pubmed', pubmed_mock)
    monkeypatch.setattr(pt, 'fetch_annotations', pubtator_mock)
    monkeypatch.setattr(mesh, 'load_mesh', mesh_mock)
    monkeypatch.setattr(taxonomy, 'load_taxonomy', taxonomy_mock)
    result = search_by_keyword('test')

    assert result['MSHD:D058729'].__dict__ == {
        '_relationship': None, 'id': 'MSHD:D058729', 'extra_relationship': {'APPEARED_IN': ['ARTI:2']}}
    assert result['MSHD:D058729'].raw_id == 'D058729'
    assert result['MSHD:D058729'].name == 'Peripheral Arterial Disease'
    assert result['MSHD:D058729'].relationship == {'APPEARED_IN': ['ARTI:2'], '_INCLUDES': ['MSHD:D050197']}
    assert result['MSHD:D058729'].tree_numbers == ['C14.907.137.126.307.500', 'C14.907.617.671']
    assert result['MSHD:D058729'].level == 4

    assert result['MSHC:C565928'].__dict__ == {
        '_relationship': None, 'id': 'MSHC:C565928', 'extra_relationship': {'APPEARED_IN': ['ARTI:2']}}
    assert result['MSHC:C565928'].raw_id == 'C565928'
    assert result['MSHC:C565928'].name == 'Atherosclerosis, Premature, with Deafness, Nephropathy, Diabetes Mellitus,' \
                                          ' Photomyoclonus, and Degenerative Neurologic Disease'
    assert result['MSHC:C565928'].relationship == {'APPEARED_IN': ['ARTI:2'],
                                                   '_CONTAINS': ['MSHD:D050197', 'MSHD:D003920']}
    assert result['MSHC:C565928'].tree_numbers == []
    assert result['MSHC:C565928'].level == 0

    assert result['GENE:58510'].__dict__ == {
        'id': 'GENE:58510', '_raw_id': '58510', '_name': 'HYPDH', 'extra_relationship': {'APPEARED_IN': ['ARTI:2']}}
    assert result['GENE:58510'].raw_id == '58510'
    assert result['GENE:58510'].name == 'HYPDH'

    assert result['ARTI:2'].__dict__ == {
        '_name': 'test title', '_raw_id': '2',
        'extra_relationship': {'_APPEARED_IN': ['MSHD:D058729', 'MSHC:C565928', 'GENE:58510', 'TAXO:9606']},
        'history': {'entrez': '1980/03/01', 'medline': ['1980/03/01'], 'pubmed': ['1980/03/01']},
        'id': 'ARTI:2', 'issue': '1', 'source': 'bion'}
    assert result['ARTI:2'].raw_id == '2'
    assert result['ARTI:2'].name == 'test title'

    assert result['TAXO:9606'].__dict__ == {
        '_relationship': None, 'id': 'TAXO:9606', 'extra_relationship': {'APPEARED_IN': ['ARTI:2']}}
    assert result['TAXO:9606'].raw_id == 9606
    assert result['TAXO:9606'].name == 'Homo sapiens'
    assert result['TAXO:9606'].relationship == {
        'APPEARED_IN': ['ARTI:2'], 'INCLUDES': ['TAXO:63221'], '_INCLUDES': ['TAXO:9605']}
    assert result['TAXO:9606'].rank == 'species'
    assert result['TAXO:9606'].family == 'Hominidae'
    assert result['TAXO:9606'].genus == 'Homo'
    assert result['TAXO:9606'].level == 64
    assert result['TAXO:9606'].lineage == ['TAXO:9605']
