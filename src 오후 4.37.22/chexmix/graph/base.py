from typing import Any, Dict, List, Optional, Tuple, Union

import networkx as nx

NodeId = Union[str, int]
NodeAttr = Dict[str, Any]
EdgeAttr = Dict[str, Any]


class Header:
    Article = 'ARTI'
    Taxonomy = 'TAXO'
    MeSHD = 'MSHD'
    MeSHC = 'MSHC'
    ChemOnto = 'CLFR'
    Chemical = 'INCK'
    Gene = 'GENE'
    Mutation = 'MUTA'


class TaxParentType:
    Genus = 'Genus'
    Family = 'Family'


class NodeType:
    Keyword = 'Keyword'
    Article = 'Article'
    Taxonomy = 'Taxonomy'
    MeSHD = 'MeSH Descriptor'
    MeSHC = 'MeSH Supplementary Record'
    Literature = 'Literature'
    ChemOnto = 'ClassyFire Chemical Ontology'
    Chemical = 'Chemical'
    Gene = 'Gene'
    Mutation = 'Mutation'


node_color_table = {
    NodeType.Keyword: 'green',
    NodeType.Article: 'blue',
    NodeType.Taxonomy: 'green',
    NodeType.MeSHC: 'blue',
    NodeType.MeSHD: 'blue',
    NodeType.Literature: 'green',
    NodeType.ChemOnto: 'green',
    NodeType.Chemical: 'blue',
    NodeType.Gene: 'blue',
    NodeType.Mutation: 'blue',
}


class EdgeType:
    MENTIONED = 'MENTIONED'
    APPEARED_IN = 'APPEARED_IN'
    IS_A = 'IS_A'
    INCLUDES = 'INCLUDES'
    CONTAINS = 'CONTAINS'
    HAS = 'HAS'

    @staticmethod
    def reverse_prefix(edge_type: str) -> str:
        if edge_type.startswith('_'):
            ret = edge_type[1:]
        else:
            ret = '_' + edge_type
        return ret


edge_color_table = {
    EdgeType.MENTIONED: '#A0A0A0',
    EdgeType.APPEARED_IN: '#006666',
    EdgeType.IS_A: '#000066',
    EdgeType.INCLUDES: '#000000',
    EdgeType.CONTAINS: '#404040',
    EdgeType.HAS: '#990000',
}


mesh_type = {
    'A': 'Anatomy',
    'B': 'Organisms',
    'C': 'Diseases',
    'D': 'Chemicals and Drugs',
    'E': 'Analytical, Diagnostic and Therapeutic Techniques, and Equipment',
    'F': 'Psychiatry and Psychology',
    'G': 'Phenomena and Processes',
    'H': 'Disciplines and Occupations',
    'I': 'Anthropology, Education, Sociology, and Social Phenomena',
    'J': 'Technology, Industry, and Agriculture',
    'K': 'Humanities',
    'L': 'Information Science',
    'M': 'Named Groups',
    'N': 'Health Care',
    'V': 'Publication Characteristics',
    'Z': 'Geographicals',
}


# pylint: disable=too-many-public-methods
class BioGraph(nx.MultiDiGraph):
    def __init__(
        self,
        nodes: Optional[List[Tuple[NodeId, NodeAttr]]] = None,
        edges: Optional[List[Tuple[NodeId, NodeId, EdgeAttr]]] = None,
    ):
        """Constructor method. Just create BioGraph objects, or build graphs with incoming node and edge information.

        :param nodes: nodes of graph
        :param edges: edges of graph
        """
        super().__init__()
        if nodes is not None:
            self.add_nodes_from(nodes)
        if edges is not None:
            self.add_edges_from(edges)

    def intersection(self, other: 'BioGraph') -> 'BioGraph':
        """Build the intersection between the two graphs.

        :param other: other graph
        :return:
        """
        intersection_graph = self.__class__()
        intersection_graph.add_edges_from(edge for edge in self.edges(data=True) if edge in other.edges(data=True))
        intersection_graph.add_nodes_from(node for node in self.nodes(data=True) if node in other.nodes(data=True))
        return intersection_graph

    def difference(self, other: 'BioGraph') -> 'BioGraph':
        """Build the difference between the two graphs. (self - other)

        :param other: other graph
        :return:
        """
        diff_graph = self.__class__()
        diff_graph.add_edges_from(edge for edge in self.edges(data=True) if edge not in other.edges(data=True))
        diff_graph.add_nodes_from(node for node in self.nodes(data=True) if node not in other.nodes(data=True))

        return diff_graph

    def union(self, other: 'BioGraph') -> 'BioGraph':
        """Build the sum of the two graphs.

        :param other: other graph
        :return:
        """
        return nx.compose(self, other)

    def threshold(self, threshold: int) -> 'BioGraph':
        """Remain only nodes with more than threshold.

        :param threshold: threshold to filter
        :return: trimmed graph
        """
        trimmed_graph = self.copy()
        for node in self:
            is_smaller_than_threshold = trimmed_graph.nodes[node]['count'] < threshold
            is_not_keyword = trimmed_graph.nodes[node]['type'] != NodeType.Keyword
            if is_smaller_than_threshold and is_not_keyword:
                trimmed_graph.remove_node(node)
        return trimmed_graph

    def find_roots(self, edge_types: Optional[List[EdgeType]] = None) -> List[NodeId]:
        """Find root nodes.

        :param edge_types: edge type for remaining
        :return: root nodes
        """
        if edge_types is not None:
            graph = self.remain_by_edge_types(edge_types)
        else:
            graph = self
        root_nodes = [node for node, degree in graph.in_degree() if degree == 0]
        return root_nodes

    def find_leaves(self, edge_types: Optional[List[EdgeType]] = None) -> List[NodeId]:
        """Find leaf nodes.

        :param edge_types: edge type for remaining
        :return: leaf nodes
        """
        if edge_types is not None:
            graph = self.remain_by_edge_types(edge_types)
        else:
            graph = self
        leaf_nodes = [node for node, degree in graph.out_degree() if degree == 0]
        return leaf_nodes

    def total_count(self, nodes: List[str]) -> int:
        """Sum nodes 'count' type.

        :param nodes: nodes
        :return: sum of 'count'
        """
        return sum(self.nodes[node]['count'] for node in nodes if 'count' in self.nodes[node])

    def draw(self, **kw_args):
        """
        graph visualization with matplotlib
        :param kw_args:
        :return:
        """
        label_name = {}
        nodes_colors = []
        for node, node_attr in self.nodes.data():
            label_name[node] = node_attr.get('name', node[5:13])
            nodes_colors.append(node_color_table[node_attr['type']])
        edges_colors = [edge_color_table[edge[2]['type']] for edge in self.edges.data()]
        nx.draw(
            self,
            labels=label_name,
            with_labels=True,
            connectionstyle="arc3,rad=-0.3",
            node_color=nodes_colors,
            edge_color=edges_colors,
            **kw_args,
        )

    def subgraph_from_roots(self, root_nodes: List[NodeId], edge_types: Optional[List[EdgeType]] = None) -> 'BioGraph':
        """Build a sub graph of root nodes and their descendants.

        :param root_nodes: root nodes
        :param edge_types: edge types for remaining
        :return: sub graph
        """
        if edge_types is not None:
            trimmed_graph = self.remain_by_edge_types(edge_types)
        else:
            trimmed_graph = self
        sub_graph = self.__class__()
        nodes, edges = self.nodes_and_edges_from_roots_or_leaves(trimmed_graph, root_nodes, 'successors')
        sub_graph.add_nodes_from(nodes)
        sub_graph.add_edges_from(edges)
        sub_graph = sub_graph.inherit_attr_from(self)
        return sub_graph

    def subgraph_from_leaves(self, leaf_nodes: List[NodeId], edge_types: Optional[List[EdgeType]] = None) -> 'BioGraph':
        """Build a sub graph of leaf nodes and their ancestors.

        :param leaf_nodes: leaf nodes
        :param edge_types: edge types for remaining
        :return: sub graph
        """
        if edge_types is not None:
            trimmed_graph = self.remain_by_edge_types(edge_types)
        else:
            trimmed_graph = self
        sub_graph = self.__class__()
        nodes, edges = self.nodes_and_edges_from_roots_or_leaves(trimmed_graph, leaf_nodes, 'predecessors')
        sub_graph.add_nodes_from(nodes)
        sub_graph.add_edges_from(edges)
        sub_graph = sub_graph.inherit_attr_from(self)
        return sub_graph

    def remain_by_edge_types(self, edge_types: List[EdgeType]) -> 'BioGraph':
        """Remain only the desired type of edge

        :param edge_types: type of edge to remain
        :return: filtered graph
        """
        edge_types = set(edge_types)
        trimmed_graph = self.__class__()
        edges = filter(lambda edge: edge[2]['type'] in edge_types, self.edges(data=True))
        trimmed_graph.add_edges_from(edges)
        trimmed_graph = trimmed_graph.inherit_attr_from(self)
        return trimmed_graph

    def remain_by_node_types(self, node_types: List[NodeType]) -> 'BioGraph':
        """Remain only the desired type of node

        :param node_types: type of node to remain
        :return: filtered graph
        """
        node_types = set(node_types)
        filtered_graph = self.copy()
        filtered_graph.remove_nodes_from(node for node in self if filtered_graph.nodes[node]['type'] not in node_types)
        return filtered_graph

    def set_attribute(self, attr_key: str, attr_value: Any, nodes: List[Union[int, str]]) -> 'BioGraph':
        """Set attribute

        :param attr_key: attribute key
        :param attr_value: attribute value
        :param nodes: target nodes
        :return:
        """
        added_graph = self.copy()
        for node in nodes:
            added_graph.nodes[node][attr_key] = attr_value
        return added_graph

    def inherit_attr_from(self, other: 'BioGraph') -> 'BioGraph':
        """Inherit attribute from other bio graph

        :param other: other graph for inherit
        :return: inherited graph
        """
        inherited_graph = self.copy()
        for node in self:
            if node in other:
                nx.set_node_attributes(inherited_graph, {node: other.nodes[node]})
        for edge in self.edges():
            if (edge in other.edges()) and (len(self.get_edge_data(edge[0], edge[1]).values()) == 0):
                for eid, e_attr in other.get_edge_data(edge[0], edge[1]).items():
                    nx.set_edge_attributes(inherited_graph, {(edge[0], edge[1], eid): e_attr})
        return inherited_graph

    def get_table(self) -> Dict[NodeId, Dict]:
        """Get table from graph.

        :return: table
        """
        nodes = self.nodes(data=True)
        edges = self.edges(data=True)
        table = {}
        for node, node_attr in nodes:
            node_attr['relationship'] = {}
            table[node] = node_attr
        for s_node, e_node, edge_attr in edges:
            edge_types = {
                'edge_type': {'edge_type': edge_attr['type'], 's_node': s_node, 'e_node': e_node},
                'reversed_edge_type': {
                    'edge_type': EdgeType.reverse_prefix(edge_attr['type']),
                    's_node': e_node,
                    'e_node': s_node,
                },
            }
            for value in edge_types.values():
                edge_type, s_node, e_node = value['edge_type'], value['s_node'], value['e_node']
                if edge_type in table[s_node]['relationship']:
                    table[s_node]['relationship'][edge_type].append(e_node)
                else:
                    table[s_node]['relationship'][edge_type] = [e_node]

        return table

    @classmethod
    def from_table(cls, table: Dict[NodeId, Dict]) -> 'BioGraph':
        """Build graph from table

        :param table: table
        :return: Bio graph
        """
        nodes, edges = BioGraph.nodes_and_edges_from_table(table)
        return cls(nodes, edges)

    @staticmethod
    def create_node_id(header: Header, raw_id: Union[int, str]) -> str:
        """create node name (ex. 'TAXO:9606', 'MESH:C01034')

        :param header: header of node
        :param raw_id: raw id
        :return: node name
        """
        return f"{header}:{raw_id}"

    @staticmethod
    def get_raw_id(node: str) -> str:
        """Get the id from the node name. (TAXO:1234 -> 1234)

        :param node: node id
        :return: raw id
        """
        raw_id = node[5:]
        raw_id = int(raw_id) if raw_id.isdecimal() else raw_id
        return raw_id

    @staticmethod
    def get_header(node: str) -> str:
        """Get the header from the node name. (TAXO:1234 -> TAXO)

        :param node: node id
        :return: header
        """
        return node[:4]

    @staticmethod
    def nodes_and_edges_from_table(table: Dict[NodeId, Dict]):
        """Create nodes and edges data with table of entities.

        :param table: table of entities
        :return: nodes and edges
        """
        nodes = []
        edges = []
        for entity_id, attributes in table.items():
            node_attr = {}
            for k, v in attributes.items():
                if (BioGraph.get_header(entity_id) == Header.MeSHC) or (k != "relationship"):
                    node_attr[k] = v
            nodes.append((entity_id, node_attr))
            relationships = attributes['relationship']
            for edge, target_nodes in relationships.items():
                if edge.startswith('_'):
                    continue
                edges.extend([(entity_id, target_node, {'type': edge}) for target_node in target_nodes])
        return nodes, edges

    @staticmethod
    def nodes_and_edges_from_roots_or_leaves(graph, target_nodes: List[NodeId], case: str) -> Tuple[List, List]:
        """Get nodes and edges from root or leaf nodes.

        :param graph: original graph
        :param target_nodes: root or leaf nodes
        :param case: "successors" or "predecessors"
        :return:
        """
        nodes = []
        edges = []
        visited = set()
        queue = target_nodes.copy()
        while queue:
            node = queue.pop()
            if (node in visited) or (node not in graph):
                continue
            visited.add(node)
            nodes.append((node, graph.nodes[node]))
            if case == "successors":
                children = list(graph.successors(node))
                queue.extend(children)
                for child_node in children:
                    for edge_attr in graph.get_edge_data(node, child_node).values():
                        edges.append((node, child_node, edge_attr))
            else:
                parents = list(graph.predecessors(node))
                queue.extend(parents)
                for parent_node in parents:
                    for edge_attr in graph.get_edge_data(parent_node, node):
                        edges.append((parent_node, node, edge_attr))
        return nodes, edges


class HierarchicalGraph(BioGraph):
    def is_descendant(self, node_id1: str, node_id2: str) -> bool:
        """return True if a node of 'node_id1' is a desecendant of that of 'node_id2'

        :param node_id1: node id
        :param node_id2: node id
        :return: bool
        """
        raise NotImplementedError('This function need to implement on inherited class')
