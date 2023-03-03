from typing import Dict, List, Union

from chexmix.graph import EdgeType
from chexmix.table.base import BaseEntity


class Publication(BaseEntity):
    @property
    def raw_id(self) -> str:
        return self._raw_id

    @property
    def name(self) -> str:
        return self._name

    def __init__(
        self,
        uid: str,
        extra_relationship: Dict[str, List[str]],
        name: str,
        source: str,
        history: Dict[str, Union[List, str]],
        issue: str,
    ):
        """Publication information from PubMed

        :param uid:                 Publication id
        :param extra_relationship:  BioEntity ids mentioned in the Publication
        :param name:                Publication Title
        :param source:              Published journal
        :param history:             Published or Registered Date
        :param issue:               issued number
        """
        super().__init__(uid, extra_relationship)
        self._raw_id = uid[5:]
        self._name = name
        self.source = source
        self.history = history
        self.issue = issue

    @staticmethod
    def uid_from(raw_id) -> str:
        return 'ARTI:' + str(raw_id)

    @staticmethod
    def normalize(entrez_table) -> Dict[str, Union[str, Dict]]:
        normed_entrez_table = {}
        for publ in entrez_table:
            uid = Publication.uid_from(publ['Id'])
            normed_entrez_table[uid] = Publication(
                uid,
                {EdgeType.reverse_prefix(EdgeType.APPEARED_IN): []},
                publ['Title'],
                publ['Source'],
                publ['History'],
                publ['Issue'],
            )
        return normed_entrez_table
