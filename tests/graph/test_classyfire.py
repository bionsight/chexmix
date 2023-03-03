from chexmix.graph import ClassyFireGraph


def test_ClassyFireGraph(classyfire_query_result):
    classyfiregraph = ClassyFireGraph.from_classyfire_entities(classyfire_query_result)
    assert dict(classyfiregraph.nodes(data=True)) == {
        'CLFR:0000001': {'level': 'kingdom', 'name': 'kd', 'chemont_id': 'CHEMONTID:0000001',
                         'lineage': [],
                         'type': 'ClassyFire Chemical Ontology'},
        'CLFR:0000011': {'level': 'superclass', 'name': 'sc', 'chemont_id': 'CHEMONTID:0000011',
                         'lineage': ['CLFR:0000001'],
                         'type': 'ClassyFire Chemical Ontology'},
        'CLFR:0000111': {'level': 'class', 'name': 'cs', 'chemont_id': 'CHEMONTID:0000111',
                         'lineage': ['CLFR:0000001', 'CLFR:0000011'],
                         'type': 'ClassyFire Chemical Ontology'},
        'INCK:ABCDEFG': {'smiles': 'smile1', 'molecular_framework': 'mol1',
                         'parent': 'CLFR:0000111', 'type': 'Chemical'},
        'CLFR:0000211': {'level': 'class', 'name': 'cs2', 'chemont_id': 'CHEMONTID:0000211',
                         'lineage': ['CLFR:0000001', 'CLFR:0000011'],
                         'type': 'ClassyFire Chemical Ontology'},
        'CLFR:0001211': {'level': 'subclass', 'name': 'sbc', 'chemont_id': 'CHEMONTID:0001211',
                         'lineage': ['CLFR:0000001', 'CLFR:0000011', 'CLFR:0000211'],
                         'type': 'ClassyFire Chemical Ontology'},
        'CLFR:0011211': {'level': 'level5', 'name': 'l5', 'chemont_id': 'CHEMONTID:0011211',
                         'lineage': ['CLFR:0000001', 'CLFR:0000011', 'CLFR:0000211', 'CLFR:0001211'],
                         'type': 'ClassyFire Chemical Ontology'},
        'CLFR:0111211': {'level': 'level6', 'name': 'l6', 'chemont_id': 'CHEMONTID:0111211',
                         'lineage': ['CLFR:0000001', 'CLFR:0000011', 'CLFR:0000211', 'CLFR:0001211', 'CLFR:0011211'],
                         'type': 'ClassyFire Chemical Ontology'},
        'CLFR:1111211': {'level': 'level7', 'name': 'l7', 'chemont_id': 'CHEMONTID:1111211',
                         'lineage': ['CLFR:0000001', 'CLFR:0000011', 'CLFR:0000211', 'CLFR:0001211',
                                     'CLFR:0011211', 'CLFR:0111211'],
                         'type': 'ClassyFire Chemical Ontology'},
        'INCK:HIJKLMN': {'smiles': 'smile2', 'molecular_framework': 'mol2',
                         'parent': 'CLFR:1111211', 'type': 'Chemical'}}
    assert list(classyfiregraph.edges(data=True)) == [
        ('CLFR:0000001', 'CLFR:0000011', {'type': 'INCLUDES'}),
        ('CLFR:0000011', 'CLFR:0000111', {'type': 'INCLUDES'}),
        ('CLFR:0000011', 'CLFR:0000211', {'type': 'INCLUDES'}),
        ('CLFR:0000111', 'INCK:ABCDEFG', {'type': 'CONTAINS'}),
        ('CLFR:0000211', 'CLFR:0001211', {'type': 'INCLUDES'}),
        ('CLFR:0001211', 'CLFR:0011211', {'type': 'INCLUDES'}),
        ('CLFR:0011211', 'CLFR:0111211', {'type': 'INCLUDES'}),
        ('CLFR:0111211', 'CLFR:1111211', {'type': 'INCLUDES'}),
        ('CLFR:1111211', 'INCK:HIJKLMN', {'type': 'CONTAINS'})]


def test_is_descendant(classyfire_query_result):
    classyfiregraph = ClassyFireGraph.from_classyfire_entities(classyfire_query_result)
    assert classyfiregraph.is_descendant('INCK:ABCDEFG', 'CLFR:0000111') and \
           classyfiregraph.is_descendant('CLFR:0111211', 'CLFR:0000211') and \
           not classyfiregraph.is_descendant('INCK:ABCDEFG', 'INCK:HIJKLMN')
