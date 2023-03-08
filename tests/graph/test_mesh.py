from chexmix.graph import MeSHGraph


def test_get_mesh_id_from(mesh_table):
    for entity_id, entity_attr in mesh_table.items():
        assert MeSHGraph.get_mesh_node_id_from(entity_attr['raw_id']) == entity_id


def test_subgraph_from_pubtator_bioentities(mesh_table):
    mesh_graph = MeSHGraph.from_table(mesh_table)
    subgraph = mesh_graph.subgraph_from_pubtator_bioentities({'D058729': 1})
    assert list(subgraph.nodes()) == ['MSHD:D058729', 'MSHD:D050197']


def test_is_descendant(mesh_table):
    mesh_graph = MeSHGraph.from_table(mesh_table)
    assert mesh_graph.is_descendant('MSHD:D058729', 'MSHD:D050197')
    assert mesh_graph.is_descendant('MSHD:D058729', 'MSHC:C565928')
