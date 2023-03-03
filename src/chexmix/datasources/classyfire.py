import logging
import uuid
from time import sleep
from typing import List

from chexmix import utils
import requests

CLASSYFIRE_URL = "http://classyfire.wishartlab.com"

log = logging.getLogger(__name__)


def query(chem_smileses: List[str], delay: float = 0.2, chunk_size: int = 10) -> List[str]:
    """
    query chemical taxonomy using claasyfire-api
    :param chem_smileses: chem_smileses is multiple line of string
    :param delay: used to reduce server load when querying
    :param chunk_size: the number of smiles for each iterator
    :return:
    """
    query_output = []
    headers = {"Content-Type": "application/json"}
    for smileses in utils.iter_grouper(chunk_size, chem_smileses):
        query_input = "\n".join(smileses)
        req_post = requests.post(  # pylint: disable=missing-timeout
            f"{CLASSYFIRE_URL}/queries.json",
            json={"label": str(uuid.uuid1()), "query_input": query_input, "query_type": "STRUCTURE"},
            headers=headers,
        )
        for _ in range(chunk_size):
            req_get = requests.get(  # pylint: disable=missing-timeout
                f'{CLASSYFIRE_URL}/queries/{req_post.json()["id"]}.json', headers=headers
            )
            if not req_get.ok:
                log.warning(f"Could not get Classyfire information for {req_post.json()['id']}")
                break
            sleep(delay)
        query_output += req_get.json()["entities"]
    return query_output
