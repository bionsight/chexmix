import uuid
from time import sleep
from typing import List

import requests
from chexmix.utils import iter_grouper

CLASSYFIRE_URL = "http://classyfire.wishartlab.com/"


def query(chem_smileses: List[str], delay: float = 0.2) -> List[str]:
    """
    query chemical taxonomy using claasyfire-api
    :param chem_smiles: chem_smiles is multiple line of string
    :param delay: used to reduce server load when querying
    :return:
    """
    query_output = []
    for smileses in iter_grouper(10, chem_smileses):
        query_input = "\n".join(smiles for smiles in smileses)
        req_post = requests.post(
            f"{CLASSYFIRE_URL}queries.json",
            json={
                "label": str(uuid.uuid1()),
                "query_input": query_input,
                "query_type": "STRUCTURE",
            },
            headers={"Content-Type": "application/json"},
        )
        while True:
            req_get = requests.get(
                f'{CLASSYFIRE_URL}queries/{req_post.json()["id"]}.json',
                headers={"Content-Type": "application/json"},
            )
            if req_get.json()["classification_status"] == "Done":
                break
            sleep(delay)
        query_output += req_get.json()["entities"]
    return query_output
