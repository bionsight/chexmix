from typing import Dict, List, Union

from chexmix.graph import EdgeType, Header, HierarchicalGraph, NodeType


class ClassyFireGraph(HierarchicalGraph):
    LEVEL_INDEX = [
        'kingdom',
        'superclass',
        'class',
        'subclass',
        'level5',
        'level6',
        'level7',
        'level8',
        'level9',
        'level10',
        'level11',
        'level12',
    ]

    @classmethod
    def from_classyfire_entities(cls, entities: List[Dict]):
        nodes, edges = [], []
        for entity in entities:
            ns, es = cls.nodes_and_edges_from_entity(entity)
            nodes += ns
            for edge in es:
                if edge not in edges:
                    edges.append(edge)
        # nodes and edges may have duplicated elements
        return cls(nodes, edges)

    @classmethod
    def nodes_and_edges_from_entity(cls, entity: Dict[str, Union[str, Dict]]):
        """
        make nodes and edges from entity queried by classyfire_API
        :param entity:
        :return:
        """
        nodes = []
        inchikey = entity['inchikey'][9:]  # InChiKey=xxx -> xxx
        lineage = []
        lineage_ids = []
        for level in ['kingdom', 'superclass', 'class', 'subclass']:
            if entity[level] == entity['direct_parent']:
                break
            lineage.append(entity[level])
        lineage += entity['intermediate_nodes']
        lineage.append(entity['direct_parent'])
        for level, node in zip(cls.LEVEL_INDEX, lineage):
            chemont_raw_id = node['chemont_id'][10:]  # CHEMONTID:xxx -> xxx
            node_id = cls.create_node_id(Header.ChemOnto, chemont_raw_id)
            node_data = {
                'level': level,
                'name': node['name'],
                'chemont_id': node['chemont_id'],
                'lineage': lineage_ids.copy(),
                'type': NodeType.ChemOnto,
            }
            nodes.append((node_id, node_data))
            lineage_ids.append(node_id)
        entity_data = {
            'smiles': entity['smiles'],
            'molecular_framework': entity['molecular_framework'],
            'parent': lineage_ids[-1],
            'type': NodeType.Chemical,
        }
        nodes.append((cls.create_node_id(Header.Chemical, inchikey), entity_data))
        edges = [
            (src_node[0], dst_node[0], {'type': EdgeType.INCLUDES}) for (src_node, dst_node) in zip(nodes, nodes[1:-1])
        ]
        if len(nodes) > 1:
            edges.append((nodes[-2][0], nodes[-1][0], {'type': EdgeType.CONTAINS}))
        return nodes, edges

    def is_descendant(self, node_id1: str, node_id2: str) -> bool:
        node_data = self.nodes.data()
        node_attrs = [
            node_data[node_attr['parent']] if node_attr['type'] == NodeType.Chemical else node_attr
            for node_attr in [node_data[node_id1], node_data[node_id2]]
        ]
        return (node_attrs[0] == node_attrs[1]) or (node_id2 in node_attrs[0]['lineage'])
