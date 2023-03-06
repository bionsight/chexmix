from typing import Union, Dict, List

from chexmix import utils
from chexmix.data import Taxonomy
from chexmix.graph import EdgeType, Header, NodeType


def create_node_id(tax_id):
    return Header.Taxonomy + ":" + str(tax_id)


@utils.cached(utils.data_file('taxonomy.pkl'))
def load_taxonomy() -> Dict[str, Union[str, int, Dict, List[Dict], List[str]]]:
    taxonomy = Taxonomy.load_taxdump()['taxonomy']
    ranks = [
        'superkingdom',
        'kingdom',
        'subkingdom',
        'superphylum',
        'phylum',
        'subphylum',
        'infraphylum',
        'superclass',
        'class',
        'subclass',
        'infraclass',
        'cohort',
        'subcohort',
        'superorder',
        'order',
        'suborder',
        'infraorder',
        'parvorder',
        'superfamily',
        'family',
        'subfamily',
        'tribe',
        'subtribe',
        'genus',
        'subgenus',
        'section',
        'subsection',
        'series',
        'subseries',
        'species group',
        'species subgroup',
        'species',
        'forma specialis',
        'subspecies',
        'varietas',
        'subvariety',
        'forma',
        'serogroup',
        'serotype',
        'strain',
        'isolate',
    ]
    node_table = {
        create_node_id(t['tax_id']): {
            'id': create_node_id(t['tax_id']),
            'raw_id': t['tax_id'],
            'type': NodeType.Taxonomy,
            'rank': t['rank'],
            'name': t['tax_name'],
            'parent_id': create_node_id(t['parent_tax_id']),
            'family': t['family'],
            'genus': t['genus'],
            'level': (ranks.index(t['rank']) + 1) * 2 if t['rank'] in ranks else 0,
            'lineage': [create_node_id(raw_id) for raw_id in t['lineage']],
            'relationship': {
                EdgeType.INCLUDES: set(),
                EdgeType.reverse_prefix(EdgeType.INCLUDES): set(),
            },
        }
        for t in taxonomy
    }

    for node_id, attr in node_table.items():
        parent_id = attr['parent_id']
        parent_node = node_table[parent_id]
        parent_node['relationship'][EdgeType.INCLUDES].add(node_id)
        attr['relationship'][EdgeType.reverse_prefix(EdgeType.INCLUDES)].add(parent_id)
        if attr['level'] == 0:
            level = 1
            while parent_id != 'TAXO:1':
                parent_level = (
                    (ranks.index(node_table[parent_id]['rank']) + 1) * 2
                    if node_table[parent_id]['rank'] in ranks
                    else 0
                )
                if parent_level > 0:
                    level = parent_level + 1
                    break
                parent_id = node_table[parent_id]['parent_id']
            attr['level'] = level
    return node_table
