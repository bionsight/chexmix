from collections import Counter
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import networkx as nx

import chexmix.datasources.entrez as ez
import chexmix.datasources.mesh as mesh
import chexmix.datasources.pubtator as pt
import chexmix.datasources.taxonomy as tax

NodeId = Union[str, int]
NodeAttr = Dict[str, Any]
EdgeAttr = Dict[str, Any]


class TaxParentType(Enum):
    Genus = 'Genus'
    Family = 'Family'


class NodeType(Enum):
    Keyword = 'Keyword'
    Article = 'Article'
    Taxonomy = 'Taxonomy'
    MeSH = 'MeSH'
    Literature = 'Literature'


class EdgeType(Enum):
    MENTIONED = 'MENTIONED'
    APPEARED_IN = 'APPEARED_IN'
    IS_A = 'IS_A'
    INCLUDES = 'INCLUDES'


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
    'Z': 'Geographicals'
}


class BioGraph(nx.DiGraph):
    def __init__(self, nodes: Optional[List[Tuple[NodeId, NodeAttr]]] = None,
                 edges: Optional[List[Tuple[NodeId, NodeId, EdgeAttr]]] = None):
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
        intersection_graph = self.copy()
        intersection_graph.remove_edges_from(edge for edge in self.edges() if edge not in other.edges())
        intersection_graph.remove_nodes_from(node for node in self if node not in other)
        return intersection_graph

    def difference(self, other: 'BioGraph') -> 'BioGraph':
        """Build the difference between the two graphs. (self - other)

        :param other: other graph
        :return:
        """
        dif_graph = self.copy()
        dif_graph.remove_nodes_from(node for node in self if node in other)
        return dif_graph

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
            if (trimmed_graph.nodes[node]['count'] < threshold) \
                    and (trimmed_graph.nodes[node]['type'] != NodeType.Keyword.value):
                trimmed_graph.remove_node(node)
        return trimmed_graph

    def find_roots(self, edge_types: Optional[List[EdgeType]] = None):
        """Find root nodes.

        :param edge_types: edge type for remaining
        :return: root nodes
        """
        if edge_types is not None:
            graph = self.remain_by_edge_types(edge_types)
        else:
            graph = self.copy()
        root_nodes = [node for node, degree in graph.in_degree() if degree == 0]
        return root_nodes

    def find_leaves(self, edge_types: Optional[List[EdgeType]] = None):
        """Find leaf nodes.

        :param edge_types: edge type for remaining
        :return: leaf nodes
        """
        if edge_types is not None:
            graph = self.remain_by_edge_types(edge_types)
        else:
            graph = self.copy()
        leaf_nodes = [node for node, degree in graph.out_degree() if degree == 0]
        return leaf_nodes

    def total_count(self, nodes: List[str]) -> int:
        """Sum nodes 'count' type.

        :param nodes: nodes
        :return: sum of 'count'
        """
        count = sum([self.nodes[node]['count'] for node in nodes if 'count' in self.nodes[node]])
        return count

    def subgraph_from_root(self, root_node, edge_types: Optional[List[EdgeType]] = None) -> 'BioGraph':
        """Build a sub graph of root node and their descendants.

        :param root_node: root node
        :param edge_types: edge type for remaining
        :return: sub graph
        """
        if edge_types is not None:
            sub_graph = self.remain_by_edge_types(edge_types)
        else:
            sub_graph = self.copy()
        descendants = nx.descendants(self, root_node)
        descendants.add(root_node)
        sub_graph.remove_nodes_from(node for node in self if node not in descendants)
        return sub_graph

    def remain_by_edge_types(self, edge_types: List[EdgeType]) -> 'BioGraph':
        """Remain only the desired type of edge

        :param edge_types: type of edge to remain
        :return: filtered graph
        """
        edge_types_value = set([edge_type.value for edge_type in edge_types])
        filtered_graph = self.copy()
        nodes_to_remove = set()  # Temporarily declared as a set() to avoid duplication.
        for node1, node2, attr in self.edges(data=True):
            if attr['type'] not in edge_types_value:
                nodes_to_remove.update([node1, node2])
        filtered_graph.remove_nodes_from(nodes_to_remove)
        return filtered_graph

    def remain_by_node_types(self, node_types: List[NodeType]) -> 'BioGraph':
        """Remain only the desired type of node

        :param node_types: type of node to remain
        :return: filtered graph
        """
        node_types_value = [node_type.value for node_type in node_types]
        filtered_graph = self.copy()
        filtered_graph.remove_nodes_from(
            node for node in self if filtered_graph.nodes[node]['type'] not in node_types_value)
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
        return inherited_graph

    @staticmethod
    def create_node_name(node_type: NodeType, node_id: Union[int, str]) -> str:
        """create node name (ex. 'TAXO:9606', 'MESH:C01034')

        :param node_type: type of node
        :param node_id: id of node
        :return: node name
        """
        node_type_value = node_type.value
        return f"{node_type_value[:4].upper()}:{node_id}"

    @staticmethod
    def get_raw_id(node: str):
        """Get the id from the node name. (TAXO:1234 -> 1234)

        :param node: node id
        :return: raw id
        """
        raw_id = node[5:]
        raw_id = int(raw_id) if raw_id.isdecimal() else raw_id
        return raw_id

    @staticmethod
    def get_header(node: str):
        """Get the header from the node name. (TAXO:1234 -> TAXO)

        :param node: node id
        :return: header
        """
        header = node[:4]
        return header


class BioEntityGraph(BioGraph):
    @staticmethod
    def nodes_and_edges_from_root_ids(ncbi_table: Dict,
                                      node_type: NodeType,
                                      edge_type: EdgeType,
                                      root_ids: List) -> Tuple[List, List]:
        """Create nodes and edges data for building the children graph of root ids by ncbi data

        :param ncbi_table: ncbi data
        :param node_type: type of ncbi
        :param edge_type: type of edge
        :param root_ids: root ids
        :return: nodes and edge with attribute
        """
        edge_type_value = edge_type.value
        node_queue = [ncbi_table[root_id] for root_id in root_ids]
        nodes, edges, visited_node_ids = [], [], set()
        while node_queue:
            node = node_queue.pop()
            node_id = node['id']
            if node_id in visited_node_ids:
                continue
            visited_node_ids.add(node_id)
            node_name = BioGraph.create_node_name(node_type, node_id)
            nodes = BioEntityGraph.__append_node_with_attr(nodes, node, node_type, node_name)
            children = node['children']
            node_queue.extend(children)
            for child in children:
                child_node_id = child['id']
                child_node_name = BioGraph.create_node_name(node_type, child_node_id)
                nodes = BioEntityGraph.__append_node_with_attr(nodes, child, node_type, child_node_name)
                edges.append((node_name, child_node_name, {'type': edge_type_value}))
        return nodes, edges

    @staticmethod
    def __append_node_with_attr(nodes: List[Tuple[NodeId, NodeAttr]],
                                node_attributes: Dict[str, Any],
                                node_type: NodeType,
                                node_name: str) -> List[Tuple[NodeId, NodeAttr]]:
        node_type_value = node_type.value
        attr = {'type': node_type_value}
        attr.update({k: v for k, v in node_attributes.items() if k != 'children'})
        nodes.append((node_name, attr))
        return nodes


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
        nodes, edges = [(keyword, {'type': NodeType.Keyword.value})], []
        for pub in pubmed_table:
            pub['type'] = NodeType.Article.value
            node_name = BioGraph.create_node_name(NodeType.Article, pub['Id'])
            nodes.append((node_name, pub))
            edges.append((keyword, node_name, {'type': EdgeType.MENTIONED.value}))
        return nodes, edges

    def to_graphml(self) -> nx.DiGraph:
        """Reduce attribute for export to .graphml. A returned graph is only used to export.

        :return: graph for export
        """
        export_graph = nx.DiGraph()
        keyword_nodes = []
        for node, attr in self.nodes().items():
            if attr['type'] == NodeType.Keyword.value:
                keyword_nodes.append((node, {'type': NodeType.Keyword.value}))
                continue
            export_graph.add_nodes_from(
                [(node, {'type': attr['type'], 'title': str(attr['Title']), 'LastAuthor': str(attr['LastAuthor'])})])
        edges = [(node1, node2, {'type': EdgeType.MENTIONED.value}) for node1, node2 in self.edges()]
        export_graph.add_nodes_from(keyword_nodes)
        export_graph.add_edges_from(edges)
        return export_graph

    def get_article_ids(self) -> List[int]:
        """Get bioentities from pubmed graph

        :return: article ids
        """
        article_ids = [int(self.get_raw_id(node)) for node in self if node.startswith('ARTI')]
        return article_ids


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
    def nodes_and_edges_from_pubtator(pubtator_table: Dict[int, List]) -> Tuple[List]:
        """Create nodes and edges data with pubtator table.

        Nodes are article or ncbi entity
        Edges are relationship article and ncbi entity
        :param pubtator_table: pubtator data
        :return: nodes and edge with attribute
        """
        bioentity_node_types = {'TAXO': NodeType.Taxonomy.value, 'MESH': NodeType.MeSH.value}
        nodes, edges = [], []
        ncbi_ids = [ncbi_id for bioentities in pubtator_table.values() for ncbi_id in bioentities]
        ncbi_id_count = Counter(ncbi_ids)
        for pubid, bioentities in pubtator_table.items():
            sub_nodes = [(bioentity, {'type': bioentity_node_types[bioentity[:4]], 'count': ncbi_id_count[bioentity]})
                         for bioentity in bioentities]
            pub_node_name = BioGraph.create_node_name(NodeType.Article, pubid)
            edges += [(node[0], pub_node_name, {'type': EdgeType.APPEARED_IN.value}) for node in sub_nodes]
            nodes += sub_nodes
            nodes.append((pub_node_name, {'type': NodeType.Article.value}))
        return nodes, edges

    def get_bioentities(self, bioentity_header: Optional[str] = None) -> Dict[int, int]:
        """Get bioentities from pubtator graph with count

        :param bioentity_header: bio entity header. (ex. TAXO, MESH)
        :return: bioentities and its count
        """
        bioentity_count = {}
        for node_id, degree in self.out_degree():
            if degree > 0:
                entity_header = self.get_header(node_id)
                entity_id = self.get_raw_id(node_id)
                if (bioentity_header is None) or (entity_header == bioentity_header):
                    bioentity_count[entity_id] = degree
        return bioentity_count


class TaxonomyGraph(BioEntityGraph):
    @classmethod
    def from_root_ids(cls, root_ids: List[int]) -> 'TaxonomyGraph':
        """Build the children graph of root nodes by taxonomy data

        :param root_ids: root ids
        :return: taxonomy graph
        """
        taxonomy_table = tax.load_taxonomy()
        nodes, edges = cls.nodes_and_edges_from_root_ids(taxonomy_table, NodeType.Taxonomy, EdgeType.INCLUDES, root_ids)
        return cls(nodes, edges)

    @classmethod
    def from_pubtator_bioentities(cls, root_type: TaxParentType,
                                  pubtator_bioentities_table: Dict[int, int],
                                  targets_to_keep: Optional[List[int]] = None,
                                  optional_type: Optional[str] = None,
                                  optional_type_targets: Optional[List] = None) -> 'TaxonomyGraph':
        """Find the root type nodes of the taxonomy entity in the pubtator.
         And build the children graph from root type nodes.

        :param root_type: root type (genus or family)
        :param pubtator_bioentities_table: bioentities table {entityId: count}
        :param targets_to_keep: target list to keep
        :param optional_type: optional type
        :param optional_type_targets: id list to replace with optional type
        :return: taxonomy graph
        """
        taxonomy_table = tax.load_taxonomy()
        if targets_to_keep is not None:
            pubtator_bioentities_table = {tax_id: count for tax_id, count in pubtator_bioentities_table.items() if
                                          tax_id in targets_to_keep}
        tax_ids = [tax_id for tax_id, count in pubtator_bioentities_table.items()]
        root_ids = cls.get_parents(tax_ids, taxonomy_table, root_type)
        nodes, edges = cls.nodes_and_edges_from_root_ids(taxonomy_table, NodeType.Taxonomy, EdgeType.INCLUDES, root_ids)
        for node, node_attr in nodes:
            node_id = int(cls.get_raw_id(node))
            if (optional_type_targets is not None) and (node_id in optional_type_targets):
                node_attr['sub_type'] = optional_type
            if node_id in pubtator_bioentities_table:
                node_attr['sub_type'] = NodeType.Literature.value
                node_attr['count'] = pubtator_bioentities_table[node_id]
            if node_id in root_ids:
                node_attr['sub_type'] = root_type.value
        return cls(nodes, edges)

    @staticmethod
    def get_parents(tax_ids: List[int],
                    taxonomy: Dict[int, Dict],
                    parent_node_type: TaxParentType) -> List[int]:
        """Delete the higher level entities than parent type from the extracted ncbi id
        and the entities not on the keeping list, and obtain the parent type of the remaining entities.

        :param tax_ids: extracted ncbi ids
        :param taxonomy: ncbi taxonomy data
        :param parent_node_type: parent node type (genus or family)
        :return: parent ids
        """
        parents = []
        node_type_value = parent_node_type.value.lower()
        for tax_id in tax_ids:
            if (tax_id in taxonomy) and (taxonomy[tax_id][node_type_value] != ''):
                parents.append(taxonomy[tax_id][node_type_value])
        parent_names = list(set(parents))
        tax_name_id = {attr['name']: tax_id for tax_id, attr in taxonomy.items()}
        parent_ids = [tax_name_id[name] for name in parent_names]
        return parent_ids


class MeSHGraph(BioEntityGraph):
    @classmethod
    def from_root_ids(cls, root_ids: List[str]) -> 'MeSHGraph':
        """Build the children graph of root nodes by mesh data

        :param root_ids: root ids
        :return: mesh graph
        """
        mesh_table = mesh.load_mesh()
        nodes, edges = cls.nodes_and_edges_from_root_ids(mesh_table, NodeType.MeSH, EdgeType.INCLUDES, root_ids)
        return cls(nodes, edges)

    @classmethod
    def from_pubtator_bioentities(cls, pubtator_bioentities_table: Dict[str, int],
                                  mesh_type_to_keep: Optional[List[str]] = None) -> 'MeSHGraph':
        """Build the mesh graph from pubtator bioentities

        :param pubtator_bioentities_table: bioentities table {entityId: count}
        :param mesh_type_to_keep: list of remaining mesh type
        :return: mesh graph
        """
        mesh_table = mesh.load_mesh()
        nodes, edges = cls.nodes_edges_from_pubtator_bioentities(mesh_table, pubtator_bioentities_table,
                                                                 mesh_type_to_keep)
        return cls(nodes, edges)

    @staticmethod
    def nodes_edges_from_pubtator_bioentities(mesh_table: Dict[str, Dict],
                                              pubtator_bioentities_table: Dict[str, int],
                                              mesh_type_to_keep: Optional[List[str]] = None) -> Tuple[List, List]:
        """Create nodes and edges data using the tree number of the mesh information in the pubtator.

        :param mesh_table: ncbi mesh data
        :param pubtator_bioentities_table: bioentities table {entityId: count}
        :param mesh_type_to_keep: list ofremaining  mesh type
        :return: nodes and edge with attribute
        """
        node_id_count, edges = {}, []
        tree_numbers = MeSHGraph.__get_tree_number(pubtator_bioentities_table, mesh_table)
        for tree_number in tree_numbers:
            if (mesh_type_to_keep is not None) and (tree_number[0] not in mesh_type_to_keep):
                continue
            trees = MeSHGraph.__decompose_tree_number(tree_number)
            target_node_id = mesh_table[trees[-1]]['id']
            target_node_name = BioGraph.create_node_name(NodeType.MeSH, target_node_id)
            count = max(node_id_count[target_node_name]['count'],
                        pubtator_bioentities_table[target_node_id]) if target_node_name in node_id_count else \
                pubtator_bioentities_table[target_node_id]
            target_node_attributes = {'name': mesh_table[trees[-1]]['name'], 'type': NodeType.MeSH.value,
                                      'sub_type': mesh_type[trees[-1][0]], 'count': count}
            node_id_count[target_node_name] = target_node_attributes
            for node1, node2 in zip(trees, trees[1:]):
                node1_id, node2_id = mesh_table[node1]['id'], mesh_table[node2]['id']
                node1_name = BioGraph.create_node_name(NodeType.MeSH, node1_id)
                node2_name = BioGraph.create_node_name(NodeType.MeSH, node2_id)
                node_count = max(node_id_count[node1_name]['count'], count) \
                    if (node1_name in node_id_count) and ('count' in node_id_count[node1_name]) else count
                node_attributes = {'name': mesh_table[node1]['name'], 'type': NodeType.MeSH.value,
                                   'sub_type': mesh_type[node1[0]], 'count': node_count}
                node_id_count[node1_name] = node_attributes
                edges.append((node1_name, node2_name, {'type': EdgeType.INCLUDES.value}))
        nodes = list(node_id_count.items())
        return nodes, edges

    @staticmethod
    def __decompose_tree_number(tree_number: str) -> List[str]:
        """Decompose the tree number ( 'D01.02.03' -> ['D01', 'D01.02', 'D01.02.03'] )

        :param tree_number: tree id of mesh data
        :return: decomposed tree numbers
        """
        tree_elements = tree_number.split('.')
        return ['.'.join(tree_elements[0:i]) for i in range(1, len(tree_elements) + 1)]

    @staticmethod
    def __get_tree_number(pubtator_bioentities_table: Dict[str, int], mesh_table: Dict[str, Dict]) -> Set[str]:
        """Get tree numbers

        :param pubtator_bioentities_table: bioentities table
        :param mesh_table: MeSH data
        :return: tree numbers
        """
        tree_numbers = set()
        for mesh_id in pubtator_bioentities_table:
            if mesh_id in mesh_table and 'tree_numbers' in mesh_table[mesh_id]:
                tree_numbers.update(mesh_table[mesh_id]['tree_numbers'])
        return tree_numbers
