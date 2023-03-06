from collections import Counter
from typing import Dict, List, Optional, Tuple

import chexmix.datasources.pubtator as pt
from chexmix.graph import BioGraph, EdgeType, Header, NodeType


class PubTatorGraph(BioGraph):
    @classmethod
    def from_article_ids(cls, article_ids: List[int]) -> 'PubTatorGraph':
        """Build pubtator graph from article ids

        :param article_ids: article ids
        :return: pubtator graph
        """
        annotations = pt.fetch_annotations(article_ids)
        pubtator_table = pt.build_annotation_table(annotations)
        nodes, edges = cls.nodes_and_edges_from_pubtator(pubtator_table)
        return cls(nodes, edges)

    @staticmethod
    def nodes_and_edges_from_pubtator(pubtator_table: Dict[int, Dict[str, Dict]]) -> Tuple[List, List]:
        """Create nodes and edges data with pubtator table.

        Nodes are article or ncbi entity
        Edges are relationship article and ncbi entity
        :param pubtator_table: pubtator data
        :return: nodes and edge with attribute
        """
        bioentity_node_types = {
            'TAXO': NodeType.Taxonomy,
            'MSHD': NodeType.MeSHD,
            'MSHC': NodeType.MeSHC,
            'GENE': NodeType.Gene,
            'MUTA': NodeType.Mutation,
        }
        nodes, edges = [], []
        ncbi_ids = [ncbi_id for bioentity_info_table in pubtator_table.values() for ncbi_id in bioentity_info_table]
        ncbi_id_count = Counter(ncbi_ids)
        visited = set()
        for pubid, bioentity_info_table in pubtator_table.items():
            sub_nodes = []
            for bioentity_id in bioentity_info_table:
                sub_node_attr = {
                    'type': bioentity_node_types[bioentity_id[:4]],
                    'count': ncbi_id_count[bioentity_id],
                    'name': bioentity_info_table[bioentity_id].get('text'),
                }
                sub_nodes.append((bioentity_id, sub_node_attr))
            pub_node_name = BioGraph.create_node_id(Header.Article, pubid)
            edges += [(node[0], pub_node_name, {'type': EdgeType.APPEARED_IN}) for node in sub_nodes]
            nodes += [(node_id, node_attr) for node_id, node_attr in sub_nodes if node_id not in visited]
            visited.update(bioentity_info_table.keys())
            nodes.append((pub_node_name, {'type': NodeType.Article}))

        return nodes, edges

    def get_bioentities(self, bioentity_headers: Optional[List[Header]] = None) -> Dict[int, int]:
        """Get bioentities from pubtator graph with count

        :param bioentity_headers: bio entity headers. (ex. TAXO, MSHC, MSHD)
        :return: bioentities and its count
        """
        bioentity_count = {}
        for node_id, degree in self.out_degree():
            if degree > 0:
                entity_header = self.get_header(node_id)
                entity_id = self.get_raw_id(node_id)
                if (bioentity_headers is None) or (entity_header in bioentity_headers):
                    bioentity_count[entity_id] = degree
        return bioentity_count
