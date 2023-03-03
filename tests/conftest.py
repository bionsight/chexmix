from chexmix.graph import BioGraph
import pytest


@pytest.fixture
def some_data():
    return "here is data"


@pytest.fixture
def pubtator_table():
    return {1: {'MSHD:D050197': {'text': ''}, 'TAXO:9606': {'text': ''}, 'MSHD:D001157': {'text': ''}},
            2: {'MSHD:D001157': {'text': ''}}, 3: {'MSHD:D001157': {'text': ''}}}


@pytest.fixture
def pubmed_table():
    return [{'Id': 11111}, {'Id': 22222}, {'Id': 33333}]


@pytest.fixture
def taxonomy_table():
    return {
        "TAXO:9605": {
            'id': 'TAXO:9605',
            'raw_id': 9605,
            'type': 'Taxonomy',
            'rank': 'genus',
            'name': 'Homo',
            'family': 'Hominidae',
            'genus': '',
            'level': 48,
            'lineage': [],
            'relationship': {'INCLUDES': ['TAXO:9606']}
        },
        "TAXO:9606": {
            'id': 'TAXO:9606',
            'raw_id': 9606,
            'type': 'Taxonomy',
            'rank': 'species',
            'name': 'Homo sapiens',
            'family': 'Hominidae',
            'genus': 'Homo',
            'level': 64,
            'lineage': ['TAXO:9605'],
            'relationship': {'INCLUDES': ['TAXO:63221'], '_INCLUDES': ['TAXO:9605']}
        },
        "TAXO:63221": {
            'id': 'TAXO:63221',
            'raw_id': 63221,
            'type': 'Taxonomy',
            'rank': 'subspecies',
            'name': 'Homo sapiens neanderthalensis',
            'family': 'Hominidae',
            'genus': 'Homo',
            'level': 68,
            'lineage': ['TAXO:9605', 'TAXO:9606'],
            'relationship': {'_INCLUDES': ['TAXO:9606']}
        }
    }


@pytest.fixture
def taxonomy_dmp_mock():
    return {
        'taxonomy': [
            {'tax_id': 33208, 'rank': 'kingdom', 'tax_name': 'Metazoa', 'parent_tax_id': 33154,
             'family': '', 'genus': '', 'lineage': [131567, 2759, 33154]},
            {'tax_id': 33154, 'rank': 'clade', 'tax_name': 'Opisthokonta', 'parent_tax_id': 2759,
             'family': '', 'genus': '', 'lineage': [131567, 2759]},
            {'tax_id': 2759, 'rank': 'superkingdom', 'tax_name': 'Eukaryota', 'parent_tax_id': 131567,
             'family': '', 'genus': '', 'lineage': [131567]},
            {'tax_id': 131567, 'rank': 'no rank', 'tax_name': 'cellular organisms', 'parent_tax_id': 1,
             'family': '', 'genus': '', 'lineage': []},
            {'tax_id': 1, 'rank': '', 'tax_name': '', 'parent_tax_id': 1, 'family': '', 'genus': '', 'lineage': []}
        ]
    }


@pytest.fixture
def mesh_table():
    return {
        'MSHD:D003920': {
            'id': 'MSHD:D003920', 'raw_id': 'D003920', 'name': 'Diabetes Mellitus',
            'tree_numbers': ['C18.452.394.750', 'C19.246'], 'level': 2,
            'relationship': {'CONTAINS': ['MSHC:C565928']}
        },
        'MSHD:D050197': {
            'id': 'MSHD:D050197', 'raw_id': 'D050197', 'name': 'Atherosclerosis',
            'tree_numbers': ['C14.907.137.126.307'], 'level': 5,
            'relationship': {'INCLUDES': ['MSHD:D058729'], 'CONTAINS': ['MSHC:C565928']}
        },
        'MSHD:D058729': {
            'id': 'MSHD:D058729', 'raw_id': 'D058729', 'name': 'Peripheral Arterial Disease',
            'tree_numbers': ['C14.907.137.126.307.500', 'C14.907.617.671'], 'level': 4,
            'relationship': {'_INCLUDES': ['MSHD:D050197']}
        },
        'MSHC:C565928': {
            'id': 'MSHC:C565928', 'raw_id': 'C565928',
            'name': 'Atherosclerosis, Premature, with Deafness, Nephropathy, Diabetes Mellitus, '
                    'Photomyoclonus, and Degenerative Neurologic Disease',
            'relationship': {'_CONTAINS': ['MSHD:D050197', 'MSHD:D003920']}
        }
    }


@pytest.fixture
def mesh_XML_mock():
    return {
        'descriptor': [
            {'DescriptorUI': 'D058729', 'DescriptorName': 'Peripheral Arterial Disease',
             'TreeNumberList': ['C14.907.137.126.307.500', 'C14.907.617.671']},
            {'DescriptorUI': 'D050197', 'DescriptorName': 'Atherosclerosis', 'TreeNumberList': ['C14.907.137.126.307']},
            {'DescriptorUI': 'D001161', 'DescriptorName': 'Arteriosclerosis', 'TreeNumberList': ['C14.907.137.126']},
            {'DescriptorUI': 'D001157', 'DescriptorName': 'Arterial Occlusive Diseases',
             'TreeNumberList': ['C14.907.137']},
            {'DescriptorUI': 'D014652', 'DescriptorName': 'Vascular Diseases', 'TreeNumberList': ['C14.907']},
            {'DescriptorUI': 'D002318', 'DescriptorName': 'Cardiovascular Diseases', 'TreeNumberList': ['C14']},
            {'DescriptorUI': 'D016491', 'DescriptorName': 'Peripheral Vascular Diseases',
             'TreeNumberList': ['C14.907.617']}
        ],
        'supplement': []
    }


@pytest.fixture
def bio_graph():
    nodes1 = [('1 : node1', {'type': 'genus', 'count': 0}),
              ('1.1 : node11', {'type': 'KPEB', 'count': 5}),
              ('2 : node2', {'type': 'genus', 'count': 0}),
              ('2.1 : node21', {'type': 'Literature', 'count': 3}),
              ('2.2 : node22', {'type': 'Literature', 'count': 1}),
              ('3 : node3', {'type': 'genus', 'count': 0})]
    nodes2 = [('2 : node2', {'type': 'genus', 'count': 0}),
              ('2.1 : node21', {'type': 'Literature', 'count': 4}),
              ('3 : node3', {'type': 'genus', 'count': 0})]
    edges1 = [('1 : node1', '1.1 : node11', {'type': 'test'}),
              ('2 : node2', '2.1 : node21', {'type': 'test'}),
              ('2 : node2', '2.1 : node21', {'type': 'test2'}),
              ('2.1 : node21', '2.2 : node22', {'type': 'test'})]
    edges2 = [('2 : node2', '2.1 : node21', {'type': 'test'})]
    graph1 = BioGraph()
    graph2 = BioGraph()
    graph1.add_nodes_from(nodes1)
    graph2.add_nodes_from(nodes2)
    graph1.add_edges_from(edges1)
    graph2.add_edges_from(edges2)
    return graph1, graph2


@pytest.fixture
def classyfire_query_result():
    return [
        {
            'inchikey': 'InChIKey=ABCDEFG',
            'kingdom': {'name': 'kd', 'chemont_id': 'CHEMONTID:0000001'},
            'superclass': {'name': 'sc', 'chemont_id': 'CHEMONTID:0000011'},
            'class': {'name': 'cs', 'chemont_id': 'CHEMONTID:0000111'},
            'intermediate_nodes': [],
            'direct_parent': {'name': 'cs', 'chemont_id': 'CHEMONTID:0000111'},
            'smiles': 'smile1',
            'molecular_framework': 'mol1'
        },
        {
            'inchikey': 'InChIKey=HIJKLMN',
            'kingdom': {'name': 'kd', 'chemont_id': 'CHEMONTID:0000001'},
            'superclass': {'name': 'sc', 'chemont_id': 'CHEMONTID:0000011'},
            'class': {'name': 'cs2', 'chemont_id': 'CHEMONTID:0000211'},
            'subclass': {'name': 'sbc', 'chemont_id': 'CHEMONTID:0001211'},
            'intermediate_nodes': [{'name': 'l5', 'chemont_id': 'CHEMONTID:0011211'},
                                   {'name': 'l6', 'chemont_id': 'CHEMONTID:0111211'}],
            'direct_parent': {'name': 'l7', 'chemont_id': 'CHEMONTID:1111211'},
            'smiles': 'smile2',
            'molecular_framework': 'mol2'
        }
    ]
