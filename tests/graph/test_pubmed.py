from chexmix.graph import PubMedGraph


def test_nodes_and_edges_from_pubmed(pubmed_table):
    nodes, edges = PubMedGraph.nodes_and_edges_from_pubmed('test', pubmed_table)
    assert len(nodes) == 4
    assert len(edges) == 3


def test_get_article_ids(pubmed_table):
    nodes, edges = PubMedGraph.nodes_and_edges_from_pubmed('test', pubmed_table)
    pubmed_graph = PubMedGraph(nodes, edges)
    article_ids = pubmed_graph.get_article_ids()
    assert len(article_ids) == 3
