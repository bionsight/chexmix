import logging

log = logging.getLogger(__name__)


def add_total_count(node):
    total_count = node.get('count', 0)
    total_count += sum(add_total_count(c) for c in node['children'] if c is not node)
    node['total_count'] = total_count
    return total_count


def add_count(node_table, annotation_table, prefix, root):
    prefix_len = len(prefix)

    for v in node_table.values():
        v['count'] = 0
        if root is not None:
            v['total_count'] = 0

    for annotations in annotation_table.values():
        for _id in annotations:
            if _id.startswith(prefix):
                annotated_id = int(_id[prefix_len:])
                if annotated_id in node_table:
                    node_table[annotated_id]['count'] += 1
                else:
                    log.warning(f'{annotated_id} does not exist')

    if root in node_table:
        add_total_count(node_table[root])

    return node_table


def add_total_pmids(node):
    total_pmids = set(node.get('pmids', []))
    total_pmids = total_pmids.union(*[add_total_pmids(c) for c in node['children'] if c is not node])
    node['total_pmids'] = total_pmids
    return total_pmids


def convert_pmid(node_table, root):
    for v in node_table.values():
        v['pmids'] = []
        if root is not None:
            v['total_pmids'] = set()
    return node_table


def add_pmids(node_table, annotation_table, prefix, root):
    prefix_len = len(prefix)
    node_table = convert_pmid(node_table, root)

    for pmid, annotations in annotation_table.items():
        for _id in annotations:
            if _id.startswith(prefix):
                annotated_id = _id[prefix_len:]
                if annotated_id[0] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    try:
                        annotated_id = int(annotated_id)
                    except ValueError:
                        log.warning(f'error in parsing id: {annotated_id}')
                        continue

                if annotated_id in node_table:
                    node_table[annotated_id]['pmids'].append(pmid)
                else:
                    log.warning(f'{annotated_id} does not exist')

    if root in node_table:
        add_total_pmids(node_table[root])

    return node_table


def trim_tree(node, min_count=1):
    children = [
        trim_tree(c, min_count=min_count)
        for c in node['children']
        if (c is not node) and (len(c['total_pmids']) >= min_count)
    ]
    node['children'] = children
    return node


def get_name(node):
    return node.get('name') or node['id']


def to_json(node, name_func=get_name, sort_key=None):
    if sort_key is not None:
        children = sorted(node['children'], key=sort_key)
    else:
        children = node['children']

    return {name_func(n): to_json(n, name_func=name_func, sort_key=sort_key) for n in children}
