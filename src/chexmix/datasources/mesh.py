import logging

import chexmix.utils as utils
from chexmix.data import MeSH

log = logging.getLogger(__name__)


def get_parent_tree_number(tree_number):
    return tree_number.rsplit('.', 1)[0]


def parse_descriptor(descriptor):
    return {
        'id': descriptor['DescriptorUI'],
        'name': descriptor['DescriptorName'],
        'tree_numbers': descriptor.get('TreeNumberList', []),
        'children': []
    }


def parse_supplement(supplement):
    return {
        'id': supplement['SupplementalRecordUI'],
        'name': supplement['SupplementalRecordName'],
        'headings': supplement['HeadingMappedToListForIndex'],
        'children': []
    }


@utils.cached(utils.data_file('mesh.pkl'))
def load_mesh():
    mt = MeSH.load_XML()

    desc = [parse_descriptor(d) for d in mt['descriptor']]
    supp = [parse_supplement(s) for s in mt['supplement']]

    node_table = {d['id']: d for d in desc}
    root = {'id': 'root', 'name': 'root', 'tree_numbers': [], 'children': []}
    node_table['root'] = root

    for d in desc:
        for tn in d['tree_numbers']:
            node_table[tn] = d

    for d in desc:
        for tn in d['tree_numbers']:
            ptn = get_parent_tree_number(tn)
            if tn != ptn:
                node_table[ptn]['children'].append(d)
            else:
                root['children'].append(d)

    node_table.update({s['id']: s for s in supp})
    for s in supp:
        for h in s['headings']:
            if h in node_table:
                node_table[h]['children'].append(s)
            else:
                log.warning(f'{h} does not exist')

    return node_table
