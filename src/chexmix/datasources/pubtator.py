import json
import logging

import requests
from tqdm.auto import tqdm

log = logging.getLogger(__name__)


def parse_payload(payload):
    annotations = [
        {
            'id': annotation['infons'].get('identifier'),
            'type': annotation['infons'].get('type'),
            'text': annotation['text'],
            'locations': annotation['locations']
        } for passage in payload.get('passages', []) for annotation in passage['annotations']]
    ret = {
        'pmid': payload['pmid'],
        'year': payload['year'],
        'annotations': annotations
    }
    return ret


def get_id(annotation):
    if annotation['id'] and annotation['id'].startswith('MESH:'):
        return annotation['id']
    headers = {'Species': 'TAXO', 'Gene': 'GENE', 'Mutation': 'MUTA'}
    annotation_header = headers.get(annotation['type'], None)
    if annotation_header is not None:
        return f'{annotation_header}:{annotation["id"]}'
    return None


def unique_ids(annotations):
    ids = [get_id(a) for a in annotations]
    ids = [i for i in ids if i is not None]
    return sorted(set(ids))


def build_annotation_table(payloads):
    annotated_publs = [parse_payload(p) for p in payloads if p is not None]
    return {annotated_publ['pmid']: unique_ids(annotated_publ['annotations']) for annotated_publ in annotated_publs}


def fetch_annotations(pmids, batch_size=1000):
    pmids = [int(i) for i in pmids]

    ret = []
    for start_idx in tqdm(range(0, len(pmids), batch_size)):
        ids = pmids[start_idx: start_idx + batch_size]
        res = requests.post(url='https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson',
                            json={'pmids': ids})

        if len(res.text) == 0:
            log.warning(f'empty result: {res.text}')
            continue

        biocs = [json.loads(p) for p in res.text.splitlines()]
        id2bioc = {int(bioc['id']): bioc for bioc in biocs}
        ret += [id2bioc.get(i) for i in ids]

    return ret
