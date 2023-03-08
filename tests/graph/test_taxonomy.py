from chexmix.graph import TaxParentType, TaxonomyGraph


def test_get_parents(taxonomy_table):
    parent_ids = TaxonomyGraph.get_parents(['TAXO:9606', 'TAXO:63221'], taxonomy_table, TaxParentType.Genus)
    assert parent_ids == ['TAXO:9605']


def test_subgraph_from_pubtator_bioentities(taxonomy_table):
    tax_graph = TaxonomyGraph.from_table(taxonomy_table)
    subgraph = tax_graph.subgraph_from_pubtator_bioentities(taxonomy_table, TaxParentType.Genus, {9606: 1})
    assert list(subgraph.nodes()) == ["TAXO:9605", "TAXO:9606", "TAXO:63221"]


def test_is_descendant(taxonomy_table):
    tax_graph = TaxonomyGraph.from_table(taxonomy_table)

    assert tax_graph.is_descendant('TAXO:9606', 'TAXO:9605') and not tax_graph.is_descendant('TAXO:9605', 'TAXO:63221')
