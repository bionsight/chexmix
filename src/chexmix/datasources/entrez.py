import logging

from Bio import Entrez
from tqdm.auto import tqdm

from chexmix import env

log = logging.getLogger(__name__)


if hasattr(env, 'entrez_api_key'):
    Entrez.api_key = env.entrez_api_key

if hasattr(env, 'email'):
    Entrez.email = env.email


def search_pubmed(term, batch_size=3000):
    log.info(f'search pubmed: {term}')
    search_handle = Entrez.esearch(db='pubmed', term=term, usehistory='y', retmax=0)
    search_result_payload = Entrez.read(search_handle)
    log.debug(f'search result: {search_result_payload}')
    total_count = int(search_result_payload['Count'])
    log.info(f'total count: {total_count}')

    ret = []
    for retstart in tqdm(range(0, total_count, batch_size)):
        summary_handle = Entrez.esummary(db='pubmed',
                                         query_key=search_result_payload['QueryKey'],
                                         WebEnv=search_result_payload['WebEnv'],
                                         retstart=retstart,
                                         retmax=batch_size,
                                         retmode='xml')
        ret += Entrez.read(summary_handle)
        summary_handle.close()

    search_handle.close()

    return ret
