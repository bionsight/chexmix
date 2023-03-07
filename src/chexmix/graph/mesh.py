from typing import Dict

from chexmix.graph import EdgeType, Header, HierarchicalGraph


class MeSHGraph(HierarchicalGraph):
    def subgraph_from_pubtator_bioentities(self, pubtator_bioentities_table: Dict[str, int]):
        """Build the mesh graph from pubtator bioentities. This graph is built with pubtator bioentity and ancestors

        :param pubtator_bioentities_table: pubtator bioentities table
        :return: sub graph
        """
        bioentities = [self.get_mesh_node_id_from(entity) for entity in pubtator_bioentities_table.keys()]
        sub_graph = self.subgraph_from_leaves(bioentities)
        for node in sub_graph:
            if node in pubtator_bioentities_table:
                sub_graph.nodes[node]['count'] = pubtator_bioentities_table[node]
        return sub_graph

    @staticmethod
    def get_mesh_node_id_from(bioentity: str):
        """Get node id.

        :param bioentity: mesh bio entity
        :return: node id
        """
        mesh_header = Header.MeSHD if bioentity[0] == "D" else Header.MeSHC
        return HierarchicalGraph.create_node_id(mesh_header, bioentity)

    def is_descendant(self, node_id1: str, node_id2: str) -> bool:
        node_data = self.nodes.data()
        descriptors = [
            node_data[node_id]['relationship'][EdgeType.reverse_prefix(EdgeType.CONTAINS)]
            if HierarchicalGraph.get_header(node_id) == Header.MeSHC
            else [node_id]
            for node_id in [node_id1, node_id2]
        ]
        for desc1 in descriptors[0]:
            for desc2 in descriptors[1]:
                for tn1 in node_data[desc1]['tree_numbers']:
                    for tn2 in node_data[desc2]['tree_numbers']:
                        if tn1.startswith(tn2):
                            return True
        return False
