from chexmix.graph import BioGraph, Header


def test_nodes_and_edges_from_table(taxonomy_table):
    nodes, edges = BioGraph.nodes_and_edges_from_table(taxonomy_table)
    assert len(nodes) == 3
    assert len(edges) == 2


def test_create_node_id():
    assert BioGraph.create_node_id(Header.Taxonomy, 9606) == "TAXO:9606"
    assert BioGraph.create_node_id(Header.MeSHD, 'D012345') == "MSHD:D012345"
    assert BioGraph.create_node_id(Header.Article, 332156) == "ARTI:332156"


def test_union(bio_graph):
    union_graph = bio_graph[0].union(bio_graph[1])
    assert len(union_graph.edges()) == 4


def test_intersection(bio_graph):
    intersection_graph = bio_graph[0].intersection(bio_graph[1])
    assert list(intersection_graph.nodes()) == ['2 : node2', '2.1 : node21', '3 : node3']
    assert list(intersection_graph.edges(data=True)) == [('2 : node2', '2.1 : node21', {'type': 'test'})]


def test_difference(bio_graph):
    difference_graph = bio_graph[0].difference(bio_graph[1])
    assert list(difference_graph.edges(data=True)) == [('1 : node1', '1.1 : node11', {'type': 'test'}),
                                                       ('2 : node2', '2.1 : node21', {'type': 'test2'}),
                                                       ('2.1 : node21', '2.2 : node22', {'type': 'test'})]


def test_find_roots(bio_graph):
    roots1 = bio_graph[0].find_roots()
    roots2 = bio_graph[1].find_roots()
    roots3 = bio_graph[0].find_roots(['test2'])
    assert roots1 == ['1 : node1', '2 : node2', '3 : node3']
    assert roots2 == ['2 : node2', '3 : node3']
    assert roots3 == ['2 : node2']


def test_find_leaves(bio_graph):
    leaves1 = bio_graph[0].find_leaves()
    leaves2 = bio_graph[1].find_leaves()
    leaves3 = bio_graph[0].find_leaves(['test2'])

    assert leaves1 == ['1.1 : node11', '2.2 : node22', '3 : node3']
    assert leaves2 == ['2.1 : node21', '3 : node3']
    assert leaves3 == ['2.1 : node21']


def test_total_count(bio_graph):
    total_count1 = bio_graph[0].total_count(['2 : node2', '2.1 : node21', '2.2 : node22'])
    total_count2 = bio_graph[1].total_count(['3 : node3'])
    assert total_count1 == 4
    assert total_count2 == 0


def test_subgraph_from_roots(bio_graph):
    sub_bio_graph1_1 = bio_graph[0].subgraph_from_roots(['1 : node1'])
    sub_bio_graph1_2 = bio_graph[0].subgraph_from_roots(['2 : node2'])
    sub_bio_graph2_1 = bio_graph[1].subgraph_from_roots(['2 : node2'])
    assert len(sub_bio_graph1_1.nodes()) == 2
    assert len(sub_bio_graph1_2.nodes()) == 3
    assert len(sub_bio_graph2_1.nodes()) == 2
    assert len(sub_bio_graph1_1.edges()) == 1
    assert len(sub_bio_graph1_2.edges()) == 3
    assert len(sub_bio_graph2_1.edges()) == 1


def test_get_table(bio_graph):
    table1 = bio_graph[0].get_table()
    table2 = bio_graph[1].get_table()
    assert len(table1) == 6
    assert len(table2) == 3
    assert len(table1['2.1 : node21']['relationship']) == 3


def test_subgraph_from_leaves(bio_graph):
    sub_bio_graph1_1 = bio_graph[0].subgraph_from_leaves(['1.1 : node11'])
    sub_bio_graph1_2 = bio_graph[0].subgraph_from_leaves(['2.2 : node22'])
    sub_bio_graph2_1 = bio_graph[1].subgraph_from_leaves(['2.1 : node21'])
    assert len(sub_bio_graph1_1.nodes()) == 2
    assert len(sub_bio_graph1_2.nodes()) == 3
    assert len(sub_bio_graph2_1.nodes()) == 2
    assert len(sub_bio_graph1_1.edges()) == 1
    assert len(sub_bio_graph1_2.edges()) == 3
    assert len(sub_bio_graph2_1.edges()) == 1
