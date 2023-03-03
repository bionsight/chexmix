import os
from typing import List

from chexmix import utils
from chexmix.env import data_path

PUBTATOR_PATH = os.path.join(data_path, 'pubtatorcentral')
BIOCONCEPTS2PUBTATOR_OFFSETS_FILENAME = os.path.join(PUBTATOR_PATH, 'bioconcepts2pubtatorcentral.offset.gz')
ENTITY_TYPES = [
    'Chemical',
    'Disease',
    'Gene',  # '3630', '18024(Tax:10090)', '6647;6648'
    'DNAMutation',  # c|SUB|C|1107|G
    'ProteinMutation',  # p|SUB|V|158|M
    'SNP',  # rs2910164
    'Species',
    'CellLine',
    'DomainMotif',
]


def get_chemical_id(entity_id):
    if entity_id == '':
        return None
    if entity_id[:5] == 'CHEBI':
        return 'ChEBI', entity_id[6:]
    if entity_id[0] == 'D' or entity_id[0] == 'C':
        return 'MeSH', entity_id
    if entity_id[:4] == 'MESH':
        return 'MeSH', entity_id[5:]
    raise Exception('Unknown ID', ('Chemical', entity_id))


def get_disease_id(entity_id):
    if entity_id == '':
        return None
    if entity_id[0] == 'D' or entity_id[0] == 'C':
        return 'MeSH', entity_id
    if entity_id[:4] == 'MESH':
        return 'MeSH', entity_id[5:]
    if entity_id[:4] == 'OMIM':
        return 'OMIM', entity_id[5:]
    raise Exception('Unknown ID', ('Disease', entity_id))


def normalize_id(entity_type, entity_id):
    """return node type and node id for a given entity type and id"""
    assert entity_type in ENTITY_TYPES, f"Unkown ID, {entity_type} {entity_id}"
    if entity_type == 'Chemical':
        return get_chemical_id(entity_id)
    if entity_type == 'Disease':
        return get_disease_id(entity_id)
    if entity_type == 'CellLine':
        return entity_type, entity_id[5:]
    if entity_type == 'Species':
        return 'Taxonomy', entity_id
    return entity_type, entity_id


def get_node_type_and_id(mention):
    try:
        node_type_and_id = normalize_id(mention['Type'], mention['ID'])
    except KeyError as ex:
        print(ex)
        node_type_and_id = None
    return node_type_and_id


def pubtator_generator(filename: str = BIOCONCEPTS2PUBTATOR_OFFSETS_FILENAME, chunk_size: int = 100000) -> List[dict]:
    """
    parse bioconcepts2pubtator_offsets, and return tables/abstract and entity tables
    """

    entity = None
    entities = []

    with utils.fopen(filename, 'r') as f:
        for line in f:
            if line == '\n':
                continue

            for ctx, tag in [('title', '|t|'), ('abstract', '|a|')]:
                pos = line.find(tag, 0, 15)
                if pos > 0:
                    if ctx == 'title':
                        pmid = int(line[:pos])
                        entity = {'PMID': pmid, 'mentions': []}
                        if chunk_size > 0 and len(entities) > 0 and len(entities) % chunk_size == 0:
                            yield entities
                            entities = []
                        entities.append(entity)

                        # text = line[pos + 3:].rstrip()
                        # entity[ctx] = text

                    # ignore abstract
                    text = line[pos + 3:].rstrip()
                    entity[ctx] = text
                    break
            else:
                # if ctx == 'pubtator':
                tokens = line.split('\t')
                assert len(tokens) == 6, Exception(Exception('Invalid format', line))
                mention = {
                    'Begin': int(tokens[1]),
                    'End': int(tokens[2]),
                    'Text': tokens[3],
                    'Type': tokens[4],
                    'ID': tokens[5].rstrip(),
                }
                node_type_and_id = get_node_type_and_id(mention)
                if node_type_and_id:
                    mention['NodeType'], mention['NodeID'] = node_type_and_id
                entity['mentions'].append(mention)

    yield entities
