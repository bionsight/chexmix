import chexmix.utils as utils
from chexmix.data import Taxonomy


@utils.cached(utils.data_file('taxonomy.pkl'))
def load_taxonomy():
    taxonomy = Taxonomy.load_taxdump()['taxonomy']

    node_table = {t['tax_id']: {'id': t['tax_id'],
                                'name': t['tax_name'],
                                'parent_id': t['parent_tax_id'],
                                'family': t['family'],
                                'genus': t['genus'],
                                'children': []} for t in taxonomy}

    for n in node_table.values():
        p = node_table[n['parent_id']]
        if p is not n:
            p['children'].append(n)

    return node_table
