import chexmix.graph as graph


def test_PubMedGraph(pubmed_table):
    nodes, edges = graph.PubMedGraph.nodes_and_edges_from_pubmed("test", pubmed_table)
    pubmed_graph = graph.PubMedGraph(nodes, edges)
    assert len(pubmed_graph.nodes()) == 4
    assert len(pubmed_graph.edges()) == 3
    assert pubmed_graph.get_article_ids() == [11111, 22222, 33333]


def test_PubTatorGraph(pubtator_table):
    nodes, edges = graph.PubTatorGraph.nodes_and_edges_from_pubtator(pubtator_table)
    pubtator_graph = graph.PubTatorGraph(nodes, edges)
    assert len(pubtator_graph.nodes()) == 7
    assert len(pubtator_graph.edges()) == 6
    assert pubtator_graph.get_bioentities() == {
        "D050197": 1,
        9606: 1,
        "D001157": 3,
        2152: 1,
    }


def test_MeSHGraph(mesh_table):
    nodes, edges = graph.MeSHGraph.nodes_and_edges_from_root_ids(
        mesh_table, graph.NodeType.MeSH, graph.EdgeType.INCLUDES, ["D001157"]
    )
    mesh_graph = graph.MeSHGraph(nodes, edges)
    assert len(mesh_graph.nodes()) == 2
    assert len(mesh_graph.edges) == 1


def test_TaxonomyGraph(taxonomy_table):
    nodes, edges = graph.TaxonomyGraph.nodes_and_edges_from_root_ids(
        taxonomy_table, graph.NodeType.Taxonomy, graph.EdgeType.INCLUDES, [9606]
    )
    tax_graph = graph.TaxonomyGraph(nodes, edges)
    assert len(tax_graph.nodes()) == 3
    assert len(tax_graph.edges()) == 2


def test_create_node_name():
    assert graph.BioGraph.create_node_name(graph.NodeType.Taxonomy, 9606) == "TAXO:9606"
    assert (
        graph.BioGraph.create_node_name(graph.NodeType.MeSH, "D012345")
        == "MESH:D012345"
    )
    assert (
        graph.BioGraph.create_node_name(graph.NodeType.Article, 332156) == "ARTI:332156"
    )


def test_intersection(bio_graph):
    intersection_graph = bio_graph[0].intersection(bio_graph[1])
    assert list(intersection_graph.edges()) == [("2 : node2", "2.1 : node21")]


def test_difference(bio_graph):
    difference_graph = bio_graph[0].difference(bio_graph[1])
    assert list(difference_graph.edges()) == [("1 : node1", "1.1 : node11")]


def test_find_roots(bio_graph):
    roots1 = bio_graph[0].find_roots()
    roots2 = bio_graph[1].find_roots()
    assert roots1 == ["1 : node1", "2 : node2"]
    assert roots2 == ["2 : node2", "3 : node3"]


def test_find_leaves(bio_graph):
    leaves1 = bio_graph[0].find_leaves()
    leaves2 = bio_graph[1].find_leaves()
    assert leaves1 == ["1.1 : node11", "2.2 : node22"]
    assert leaves2 == ["2.1 : node21", "3 : node3"]


def test_total_count(bio_graph):
    total_count1 = bio_graph[0].total_count(
        ["2 : node2", "2.1 : node21", "2.2 : node22"]
    )
    total_count2 = bio_graph[1].total_count(["3 : node3"])
    assert total_count1 == 4
    assert total_count2 == 0


def test_subgraph_from_root(bio_graph):
    sub_bio_graph1_1 = bio_graph[0].subgraph_from_root("1 : node1")
    sub_bio_graph1_2 = bio_graph[0].subgraph_from_root("2 : node2")
    sub_bio_graph2_1 = bio_graph[1].subgraph_from_root("2 : node2")
    assert len(sub_bio_graph1_1.nodes()) == 2
    assert len(sub_bio_graph1_2.nodes()) == 3
    assert len(sub_bio_graph2_1.nodes()) == 2
    assert len(sub_bio_graph1_1.edges()) == 1
    assert len(sub_bio_graph1_2.edges()) == 2
    assert len(sub_bio_graph2_1.edges()) == 1


def test_get_table(bio_graph):
    table1 = bio_graph[0].get_table()
    table2 = bio_graph[1].get_table()
    assert len(table1) == 5
    assert len(table2) == 3
    assert len(table1['2.1 : node21']['relationship']) == 2


def test_ClassyFireGraph(classyfire_query_result):
    classyfiregraph = graph.ClassyFireGraph.from_classyfire_entities(
        classyfire_query_result
    )
    assert dict(classyfiregraph.nodes(data=True)) == {
        "CLFR:0000001": {
            "level": "kingdom",
            "name": "kd",
            "chemont_id": "CHEMONTID:0000001",
            "lineage": [],
            "type": "ClassyFire Chemical Ontology",
        },
        "CLFR:0000011": {
            "level": "superclass",
            "name": "sc",
            "chemont_id": "CHEMONTID:0000011",
            "lineage": ["CLFR:0000001"],
            "type": "ClassyFire Chemical Ontology",
        },
        "CLFR:0000111": {
            "level": "class",
            "name": "cs",
            "chemont_id": "CHEMONTID:0000111",
            "lineage": ["CLFR:0000001", "CLFR:0000011"],
            "type": "ClassyFire Chemical Ontology",
        },
        "INCK:ABCDEFG": {
            "smiles": "smile1",
            "molecular_framework": "mol1",
            "parent": "CLFR:0000111",
            "type": "Chemical",
        },
        "CLFR:0000211": {
            "level": "class",
            "name": "cs2",
            "chemont_id": "CHEMONTID:0000211",
            "lineage": ["CLFR:0000001", "CLFR:0000011"],
            "type": "ClassyFire Chemical Ontology",
        },
        "CLFR:0001211": {
            "level": "subclass",
            "name": "sbc",
            "chemont_id": "CHEMONTID:0001211",
            "lineage": ["CLFR:0000001", "CLFR:0000011", "CLFR:0000211"],
            "type": "ClassyFire Chemical Ontology",
        },
        "CLFR:0011211": {
            "level": "level5",
            "name": "l5",
            "chemont_id": "CHEMONTID:0011211",
            "lineage": ["CLFR:0000001", "CLFR:0000011", "CLFR:0000211", "CLFR:0001211"],
            "type": "ClassyFire Chemical Ontology",
        },
        "CLFR:0111211": {
            "level": "level6",
            "name": "l6",
            "chemont_id": "CHEMONTID:0111211",
            "lineage": [
                "CLFR:0000001",
                "CLFR:0000011",
                "CLFR:0000211",
                "CLFR:0001211",
                "CLFR:0011211",
            ],
            "type": "ClassyFire Chemical Ontology",
        },
        "CLFR:1111211": {
            "level": "level7",
            "name": "l7",
            "chemont_id": "CHEMONTID:1111211",
            "lineage": [
                "CLFR:0000001",
                "CLFR:0000011",
                "CLFR:0000211",
                "CLFR:0001211",
                "CLFR:0011211",
                "CLFR:0111211",
            ],
            "type": "ClassyFire Chemical Ontology",
        },
        "INCK:HIJKLMN": {
            "smiles": "smile2",
            "molecular_framework": "mol2",
            "parent": "CLFR:1111211",
            "type": "Chemical",
        },
    }
    assert list(classyfiregraph.edges(data=True)) == [
        ("CLFR:0000001", "CLFR:0000011", {"type": "INCLUDES"}),
        ("CLFR:0000011", "CLFR:0000111", {"type": "INCLUDES"}),
        ("CLFR:0000011", "CLFR:0000211", {"type": "INCLUDES"}),
        ("CLFR:0000111", "INCK:ABCDEFG", {"type": "CONTAINS"}),
        ("CLFR:0000211", "CLFR:0001211", {"type": "INCLUDES"}),
        ("CLFR:0001211", "CLFR:0011211", {"type": "INCLUDES"}),
        ("CLFR:0011211", "CLFR:0111211", {"type": "INCLUDES"}),
        ("CLFR:0111211", "CLFR:1111211", {"type": "INCLUDES"}),
        ("CLFR:1111211", "INCK:HIJKLMN", {"type": "CONTAINS"}),
    ]


def test_is_descendant(classyfire_query_result):
    classyfiregraph = graph.ClassyFireGraph.from_classyfire_entities(
        classyfire_query_result
    )
    assert (
        classyfiregraph.is_descendant("INCK:ABCDEFG", "CLFR:0000111")
        and classyfiregraph.is_descendant("CLFR:0111211", "CLFR:0000211")
        and not classyfiregraph.is_descendant("INCK:ABCDEFG", "INCK:HIJKLMN")
    )
