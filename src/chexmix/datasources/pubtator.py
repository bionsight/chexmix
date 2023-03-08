import json
import logging
from typing import List, Dict, Union, Optional

import requests
from chexmix.graph.base import BioGraph, Header
from chexmix.graph.mesh import MeSHGraph
from tqdm.auto import tqdm

log = logging.getLogger(__name__)


def parse_payload(payload: Dict[str, Union[str, Dict, List[Dict], int]]):
    annotations = [
        {
            'id': annotation['infons'].get('identifier'),
            'type': annotation['infons'].get('type'),
            'text': annotation['text'],
            'locations': annotation['locations'],
        }
        for passage in payload.get('passages', [])
        for annotation in passage['annotations']
    ]
    return {'pmid': payload['pmid'], 'year': payload['year'], 'annotations': annotations}


def get_id(annotation: Dict) -> Optional[str]:
    anno_id = annotation['id']
    header = {'Species': Header.Taxonomy, 'Gene': Header.Gene, 'Mutation': Header.Mutation}
    annotation_header = header.get(annotation['type'], None)
    if anno_id and anno_id.startswith('MESH:'):
        return MeSHGraph.get_mesh_node_id_from(anno_id[5:])
    return BioGraph.create_node_id(annotation_header, anno_id) if annotation_header and anno_id else None


def build_annotation_table(payloads: Dict) -> Dict[str, List[Dict]]:
    annotated_publs = [parse_payload(p) for p in payloads if p]
    return {
        annotated_publ['pmid']: {
            get_id(annotation): annotation for annotation in annotated_publ['annotations'] if get_id(annotation)
        }
        for annotated_publ in annotated_publs
    }


def fetch_annotations(pmids: List[str], batch_size=1000) -> List[Dict]:
    pmids = [int(i) for i in pmids]

    ret = []
    for start_idx in tqdm(range(0, len(pmids), batch_size)):
        # below line is a false-positive of black. fix this later
        ids = pmids[start_idx: start_idx + batch_size]  # fmt: skip
        url = 'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson'
        res = requests.post(url=url, json={'pmids': ids})  # pylint: disable=missing-timeout

        if len(res.text) == 0:
            log.warning(f'empty result: {res.text}')
            continue

        biocs = [json.loads(p) for p in res.text.splitlines()]
        id2bioc = {int(bioc['id']): bioc for bioc in biocs}
        ret += [id2bioc.get(i) for i in ids]

    return ret
