from chexmix.graph import PubTatorGraph


def test_nodes_and_edges_from_pubtator(pubtator_table):
    nodes, edges = PubTatorGraph.nodes_and_edges_from_pubtator(pubtator_table)
    assert nodes == [('MSHD:D050197', {'name': '', 'type': 'MeSH Descriptor', 'count': 1}),
                     ('TAXO:9606', {'name': '', 'type': 'Taxonomy', 'count': 1}),
                     ('MSHD:D001157', {'name': '', 'type': 'MeSH Descriptor', 'count': 3}),
                     ('ARTI:1', {'type': 'Article'}),
                     ('ARTI:2', {'type': 'Article'}),
                     ('ARTI:3', {'type': 'Article'})]
    assert edges == [('MSHD:D050197', 'ARTI:1', {'type': 'APPEARED_IN'}),
                     ('TAXO:9606', 'ARTI:1', {'type': 'APPEARED_IN'}),
                     ('MSHD:D001157', 'ARTI:1', {'type': 'APPEARED_IN'}),
                     ('MSHD:D001157', 'ARTI:2', {'type': 'APPEARED_IN'}),
                     ('MSHD:D001157', 'ARTI:3', {'type': 'APPEARED_IN'})]


def test_get_bioentities(pubtator_table):
    nodes, edges = PubTatorGraph.nodes_and_edges_from_pubtator(pubtator_table)
    pubtator_graph = PubTatorGraph(nodes, edges)

    assert pubtator_graph.get_bioentities() == {'D050197': 1, 9606: 1, 'D001157': 3}
    assert pubtator_graph.get_bioentities('TAXO') == {9606: 1}
