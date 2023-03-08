import logging
from typing import Dict, Union, List

from chexmix import utils
from chexmix.data import MeSH
from chexmix.graph import EdgeType, NodeType, MeSHGraph

log = logging.getLogger(__name__)


def get_parent_tree_number(tree_number: str) -> str:
    return tree_number.rsplit('.', 1)[0]


def parse_descriptor(
    descriptor: Dict[str, Union[str, List[Dict], List[str]]]
) -> Dict[str, Union[str, Dict[str, List[str]]]]:
    return {
        'id': MeSHGraph.get_mesh_node_id_from(descriptor['DescriptorUI']),
        'raw_id': descriptor['DescriptorUI'],
        'name': descriptor['DescriptorName'],
        'type': NodeType.MeSHD,
        'tree_numbers': descriptor.get('TreeNumberList', []),
        'relationship': {EdgeType.INCLUDES: [], EdgeType.reverse_prefix(EdgeType.INCLUDES): [], EdgeType.CONTAINS: []},
    }


def parse_supplement(
    supplement: Dict[str, Union[str, List[Dict], List[str]]]
) -> Dict[str, Union[str, Dict[str, List[str]]]]:
    return {
        'id': MeSHGraph.get_mesh_node_id_from(supplement['SupplementalRecordUI']),
        'raw_id': supplement['SupplementalRecordUI'],
        'name': supplement['SupplementalRecordName'],
        'type': NodeType.MeSHC,
        'relationship': {
            EdgeType.reverse_prefix(EdgeType.CONTAINS): list(
                map(MeSHGraph.get_mesh_node_id_from, supplement['HeadingMappedToListForIndex'])
            )
        },
    }


@utils.cached(utils.data_file('mesh.pkl'))
def load_mesh() -> Dict[str, Union[str, List[str], List[Dict]]]:
    mt = MeSH.load_XML()

    desc = [parse_descriptor(d) for d in mt['descriptor']]
    supp = [parse_supplement(s) for s in mt['supplement']]
    node_table = {d['id']: d for d in desc}
    tree_number_table = {}

    for d in desc:
        tree_numbers = d['tree_numbers']
        node_table[d['id']]['level'] = (
            min(map(lambda x: x.count('.') + 1, tree_numbers)) if len(tree_numbers) > 0 else 0
        )
        for tn in tree_numbers:
            tree_number_table[tn] = d

    visited = set()
    for d in desc:
        for tn in d['tree_numbers']:
            ptn = get_parent_tree_number(tn)
            ptn_id, tn_id = tree_number_table[ptn]['id'], tree_number_table[tn]['id']
            if (tn == ptn) or ((ptn_id, tn_id) in visited):
                continue
            visited.add((ptn_id, tn_id))
            node_table[tn_id]['relationship'][EdgeType.reverse_prefix(EdgeType.INCLUDES)].append(ptn_id)
            node_table[ptn_id]['relationship'][EdgeType.INCLUDES].append(tn_id)

    node_table.update({s['id']: s for s in supp})
    for s in supp:
        for h in s['relationship'][EdgeType.reverse_prefix(EdgeType.CONTAINS)]:
            if h in node_table:
                node_table[h]['relationship'][EdgeType.CONTAINS].append(s['id'])
            else:
                log.warning(f'{h} does not exist')

    return node_table
