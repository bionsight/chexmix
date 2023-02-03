import logging
import uuid
from time import sleep
from typing import List

import requests

from chexmix.utils import iter_grouper

log = logging.getLogger(__name__)

CLASSYFIRE_URL = "http://classyfire.wishartlab.com"


def query(chem_smileses: List[str], delay: float = 0.2, chunk_size: int = 10) -> List[str]:
    """
    query chemical taxonomy using claasyfire-api
    :param chem_smiles: chem_smiles is multiple line of string
    :param delay: used to reduce server load when querying
    :param chunk_size: chunk_size for each group
    :return:
    """
    query_output = []
    headers = {"Content-Type": "application/json"}
    for smileses in iter_grouper(chunk_size, chem_smileses):
        query_input = "\n".join(smiles for smiles in smileses)
        req_post = requests.post(
            f"{CLASSYFIRE_URL}/queries.json",
            json={"label": str(uuid.uuid1()), "query_input": query_input, "query_type": "STRUCTURE"},
            headers=headers,
        )
        for _ in range(chunk_size):
            req_get = requests.get(
                f'{CLASSYFIRE_URL}/queries/{req_post.json()["id"]}.json', headers=headers
            )
            if not req_get.ok:
                log.warning(f"Could not get Classyfire information for {smileses}")
                break
            sleep(delay)
        query_output += req_get.json()["entities"]
    return query_output
