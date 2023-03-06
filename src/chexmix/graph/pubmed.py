from typing import Dict, List, Tuple

import chexmix.datasources.entrez as ez
import networkx as nx
from chexmix.graph import BioGraph, EdgeType, Header, NodeType


class PubMedGraph(BioGraph):
    @classmethod
    def from_keyword(cls, keyword: str) -> 'PubMedGraph':
        """Build pubmed graph.

        :param keyword: keyword
        :return: pubmed graph
        """
        pubmed_table = ez.search_pubmed(keyword)
        nodes, edges = cls.nodes_and_edges_from_pubmed(keyword, pubmed_table)
        return cls(nodes, edges)

    @staticmethod
    def nodes_and_edges_from_pubmed(keyword: str, pubmed_table: List[Dict]) -> Tuple[List, List]:
        """Create node list and edge list with pubmed table

        :param keyword: keyword
        :param pubmed_table: pubmed data
        :return: nodes and edge with attribute
        """
        nodes, edges = [(keyword, {'type': NodeType.Keyword})], []
        for pub in pubmed_table:
            pub['type'] = NodeType.Article
            node_name = BioGraph.create_node_id(Header.Article, pub['Id'])
            nodes.append((node_name, pub))
            edges.append((keyword, node_name, {'type': EdgeType.MENTIONED}))
        return nodes, edges

    def to_graphml(self) -> nx.DiGraph:
        """Reduce attribute for export to .graphml. A returned graph is only used to export.

        :return: graph for export
        """
        export_graph = nx.DiGraph()

        for node, attrs in self.nodes().items():
            attr = {k: dtype(v) for k, v in attrs.items() for dtype in (str, int, float, bool) if isinstance(v, dtype)}
            export_graph.add_nodes_from([(node, attr)])
        edges = [(node1, node2, {'type': EdgeType.MENTIONED}) for node1, node2 in self.edges()]
        export_graph.add_edges_from(edges)
        return export_graph

    def get_article_ids(self) -> List[int]:
        """Get bioentities from pubmed graph

        :return: article ids
        """
        return [int(self.get_raw_id(node)) for node in self if node.startswith('ARTI')]
