from typing import Dict, Union

import chexmix.datasources.entrez as ez
import chexmix.datasources.pubtator as pt
from chexmix.table.gene import Gene
from chexmix.table.mesh import MeSH
from chexmix.table.publication import Publication
from chexmix.table.taxonomy import Taxonomy


def search_by_keyword(keyword: str) -> Dict[str, Union[str, Dict]]:
    """Pubmed search by keyword, than Pubtator query by pmid. Make a bio entity table using pubtator query data.

    :param keyword: keyword for putator search
    :return:        Entity table
    """
    entrez_table = ez.search_pubmed(keyword)
    pmids = [publ['Id'] for publ in entrez_table]
    pub_table = pt.build_annotation_table(pt.fetch_annotations(pmids))

    bio_table = Publication.normalize(entrez_table)
    entity_type_table = {'Chemical': MeSH, 'Disease': MeSH, 'Gene': Gene, 'Mutation': Gene, 'Species': Taxonomy}
    for pmid, bio_entities in pub_table.items():
        publication_id = Publication.uid_from(pmid)
        for bio_id, bio_entity_info in bio_entities.items():
            bio_type = bio_entity_info['type']
            if MeSH.is_MeSH(bio_id) and (not MeSH.is_exist(bio_id)):
                continue
            bio_table[publication_id].extra_relationship['_APPEARED_IN'].append(bio_id)
            if bio_id in bio_table:
                bio_table[bio_id].extra_relationship['APPEARED_IN'].append(publication_id)
            elif bio_type in ['Gene', 'Mutation']:
                bio_table[bio_id] = entity_type_table[bio_type](
                    bio_id, bio_entity_info['text'], {'APPEARED_IN': [publication_id]}
                )
            else:
                bio_table[bio_id] = entity_type_table[bio_type](bio_id, {'APPEARED_IN': [publication_id]})
    return bio_table
