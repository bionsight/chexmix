import pytest

import chexmix.graph as graph


@pytest.fixture
def some_data():
    return "here is data"


@pytest.fixture
def pubtator_table():
    return {
        1: ["MESH:D050197", "TAXO:9606", "MESH:D001157"],
        2: ["MESH:D001157", "GENE:2152"],
        3: ["MESH:D001157"],
    }


@pytest.fixture
def pubmed_table():
    return [{"Id": 11111}, {"Id": 22222}, {"Id": 33333}]


@pytest.fixture
def taxonomy_table():
    return {
        9606: {
            "id": 9606,
            "name": "Homo sapiens",
            "parent_id": 9605,
            "family": "Hominidae",
            "genus": "Homo",
            "children": [
                {
                    "id": 63221,
                    "name": "Homo sapiens neanderthalensis",
                    "parent_id": 9606,
                    "family": "Hominidae",
                    "genus": "Homo",
                    "children": [],
                },
                {
                    "id": 741158,
                    "name": "Homo sapiens subsp. 'Denisova'",
                    "parent_id": 9606,
                    "family": "Hominidae",
                    "genus": "Homo",
                    "children": [],
                },
            ],
        },
        63221: {
            "id": 63221,
            "name": "Homo sapiens neanderthalensis",
            "parent_id": 9606,
            "family": "Hominidae",
            "genus": "Homo",
            "children": [],
        },
        741158: {
            "id": 741158,
            "name": "Homo sapiens subsp. 'Denisova'",
            "parent_id": 9606,
            "family": "Hominidae",
            "genus": "Homo",
            "children": [],
        },
    }


@pytest.fixture
def mesh_table():
    return {
        "D050197": {
            "id": "D050197",
            "name": "Atherosclerosis",
            "tree_numbers": ["C14.907.137.126.307"],
            "children": [],
        },
        "C14.907.137.126.307": {
            "id": "D050197",
            "name": "Atherosclerosis",
            "children": [],
        },
        "C14.907.137.126": {
            "id": "D001161",
            "name": "Arteriosclerosis",
            "children": [],
        },
        "C14.907.137": {
            "id": "D001157",
            "name": "Arterial Occlusive Diseases",
            "children": [],
        },
        "C14.907": {"id": "D014652", "name": "Vascular Diseases", "children": []},
        "C14": {"id": "D002318", "name": "Cardiovascular Diseases", "children": []},
        "D001157": {
            "id": "D001157",
            "name": "Arterial Occlusive Diseases",
            "tree_numbers": ["C14.907.137"],
            "children": [{"id": "D001158", "name": "test", "children": []}],
        },
    }


@pytest.fixture
def bio_graph():
    nodes1 = [
        ("1 : node1", {"type": "genus", "count": 0}),
        ("1.1 : node11", {"type": "KPEB", "count": 5}),
        ("2 : node2", {"type": "genus", "count": 0}),
        ("2.1 : node21", {"type": "Literature", "count": 3}),
        ("2.2 : node22", {"type": "Literature", "count": 1}),
    ]
    nodes2 = [
        ("2 : node2", {"type": "genus", "count": 0}),
        ("2.1 : node21", {"type": "Literature", "count": 4}),
        ("3 : node3", {"type": "genus", "count": 0}),
    ]
    edges1 = [
        ("1 : node1", "1.1 : node11", {"type": "test"}),
        ("2 : node2", "2.1 : node21", {"type": "test"}),
        ("2.1 : node21", "2.2 : node22", {"type": "test"}),
    ]
    edges2 = [("2 : node2", "2.1 : node21", {"type": "test"})]
    graph1 = graph.BioGraph()
    graph2 = graph.BioGraph()
    graph1.add_nodes_from(nodes1)
    graph2.add_nodes_from(nodes2)
    graph1.add_edges_from(edges1)
    graph2.add_edges_from(edges2)
    return graph1, graph2


@pytest.fixture
def classyfire_query_result():
    return [
        {
            "inchikey": "InChIKey=ABCDEFG",
            "kingdom": {"name": "kd", "chemont_id": "CHEMONTID:0000001"},
            "superclass": {"name": "sc", "chemont_id": "CHEMONTID:0000011"},
            "class": {"name": "cs", "chemont_id": "CHEMONTID:0000111"},
            "intermediate_nodes": [],
            "direct_parent": {"name": "cs", "chemont_id": "CHEMONTID:0000111"},
            "smiles": "smile1",
            "molecular_framework": "mol1",
        },
        {
            "inchikey": "InChIKey=HIJKLMN",
            "kingdom": {"name": "kd", "chemont_id": "CHEMONTID:0000001"},
            "superclass": {"name": "sc", "chemont_id": "CHEMONTID:0000011"},
            "class": {"name": "cs2", "chemont_id": "CHEMONTID:0000211"},
            "subclass": {"name": "sbc", "chemont_id": "CHEMONTID:0001211"},
            "intermediate_nodes": [
                {"name": "l5", "chemont_id": "CHEMONTID:0011211"},
                {"name": "l6", "chemont_id": "CHEMONTID:0111211"},
            ],
            "direct_parent": {"name": "l7", "chemont_id": "CHEMONTID:1111211"},
            "smiles": "smile2",
            "molecular_framework": "mol2",
        },
    ]
