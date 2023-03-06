from typing import Dict, List, Optional

from chexmix.graph import Header, HierarchicalGraph, NodeType, TaxParentType


class TaxonomyGraph(HierarchicalGraph):
    def subgraph_from_pubtator_bioentities(
        self,
        taxonomy_table: Dict[int, Dict],
        root_type: TaxParentType,
        pubtator_bioentities_table: Dict[int, int],
        targets_to_keep: Optional[List[int]] = None,
        optional_type: Optional[str] = None,
        optional_type_targets: Optional[List] = None,
    ) -> 'TaxonomyGraph':
        """Find the root type nodes of the taxonomy entity in the pubtator.
         And build the children graph from root type nodes.

        :param taxonomy_table: taxonomy table
        :param root_type: root type (genus or family)
        :param pubtator_bioentities_table: bioentities table {entityId: count}
        :param targets_to_keep: target list to keep
        :param optional_type: optional type
        :param optional_type_targets: id list to replace with optional type
        :return: taxonomy graph
        """
        if targets_to_keep is not None:
            pubtator_bioentities_table = {
                tax_id: count for tax_id, count in pubtator_bioentities_table.items() if tax_id in targets_to_keep
            }
        tax_ids = [self.create_node_id(Header.Taxonomy, tax_id) for tax_id in pubtator_bioentities_table]
        root_ids = self.get_parents(tax_ids, taxonomy_table, root_type)
        sub_graph = self.subgraph_from_roots(root_nodes=root_ids, edge_types=None)
        for node in sub_graph:
            raw_id = int(self.get_raw_id(node))
            if (optional_type_targets is not None) and (raw_id in optional_type_targets):
                sub_graph.nodes[node]['sub_type'] = optional_type
            if raw_id in pubtator_bioentities_table:
                sub_graph.nodes[node]['sub_type'] = NodeType.Literature
                sub_graph.nodes[node]['count'] = pubtator_bioentities_table[raw_id]
            if node in root_ids:
                sub_graph.nodes[node]['sub_type'] = root_type
        return sub_graph

    @staticmethod
    def get_parents(tax_ids: List[int], taxonomy: Dict[int, Dict], parent_node_type: TaxParentType) -> List[int]:
        """Delete the higher level entities than parent type from the extracted ncbi id
        and the entities not on the keeping list, and obtain the parent type of the remaining entities.

        :param tax_ids: extracted ncbi ids
        :param taxonomy: ncbi taxonomy data
        :param parent_node_type: parent node type (genus or family)
        :return: parent ids
        """
        parents = []
        node_type_value = parent_node_type.lower()
        for tax_id in tax_ids:
            if (tax_id in taxonomy) and (taxonomy[tax_id][node_type_value] != ''):
                parents.append(taxonomy[tax_id][node_type_value])
        parent_names = list(set(parents))
        tax_name_id = {attr['name']: tax_id for tax_id, attr in taxonomy.items()}
        parent_ids = [tax_name_id[name] for name in parent_names]
        return parent_ids

    def is_descendant(self, node_id1: str, node_id2: str) -> bool:
        return node_id2 in self.nodes.data()[node_id1]['lineage']
