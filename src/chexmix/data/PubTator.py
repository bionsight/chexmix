import os

import chexmix.utils as utils
from chexmix.env import data_path

PUBTATOR_PATH = os.path.join(data_path, 'pubtatorcentral')
BIOCONCEPTS2PUBTATOR_OFFSETS_FILENAME = os.path.join(PUBTATOR_PATH, 'bioconcepts2pubtatorcentral.offset.gz')


def normalize_id(entity_type, entity_id):
    """return node type and node id for a given entity type and id"""
    if entity_type == 'Chemical':
        if entity_id == '':
            return None
        if entity_id[:5] == 'CHEBI':
            return 'ChEBI', entity_id[6:]
        elif entity_id[0] == 'D' or entity_id[0] == 'C':
            return 'MeSH', entity_id
        elif entity_id[:4] == 'MESH':
            return 'MeSH', entity_id[5:]
        raise Exception('Unknown ID', (entity_type, entity_id))
    elif entity_type == 'Disease':
        if entity_id == '':
            return None
        if entity_id[0] == 'D' or entity_id[0] == 'C':
            return 'MeSH', entity_id
        if entity_id[:4] == 'MESH':
            return 'MeSH', entity_id[5:]
        elif entity_id[:4] == 'OMIM':
            return 'OMIM', entity_id[5:]
        raise Exception('Unknown ID', (entity_type, entity_id))
    elif entity_type == 'Gene':
        # '3630', '18024(Tax:10090)', '6647;6648',
        return 'Gene', entity_id
    elif entity_type == 'DNAMutation':
        # c|SUB|C|1107|G
        return 'DNAMutation', entity_id
    elif entity_type == 'ProteinMutation':
        # p|SUB|V|158|M
        return 'ProteinMutation', entity_id
    elif entity_type == 'SNP':
        # rs2910164
        return 'SNP', entity_id
    elif entity_type == 'Species':
        return 'Taxonomy', entity_id
    elif entity_type == 'CellLine':
        return 'CellLine', entity_id[5:]
    elif entity_type == 'DomainMotif':
        return 'DomainMotif', entity_id
    raise Exception('Unknown ID', (entity_type, entity_id))


def pubtator_generator(filename=BIOCONCEPTS2PUBTATOR_OFFSETS_FILENAME,
                       chunk_size=100000):
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
                        entity = {'PMID': pmid,
                                  'mentions': []}
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
                if len(tokens) != 6:
                    raise Exception('Invalid format', line)

                mention = {'Begin': int(tokens[1]),
                           'End': int(tokens[2]),
                           'Text': tokens[3],
                           'Type': tokens[4],
                           'ID': tokens[5].rstrip()}
                try:
                    node_type_and_id = normalize_id(mention['Type'], mention['ID'])
                except Exception as ex:
                    print(ex)
                    node_type_and_id = None
                if node_type_and_id:
                    mention['NodeType'], mention['NodeID'] = node_type_and_id
                entity['mentions'].append(mention)

    yield entities
