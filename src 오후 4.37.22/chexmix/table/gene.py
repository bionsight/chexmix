from typing import Dict, List

from chexmix.table.base import BaseEntity


class Gene(BaseEntity):
    @property
    def raw_id(self) -> str:
        return self._raw_id

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, uid: str, name: str, extra_relationship: Dict[str, List[str]]):
        """Gene or Mutation information from Gene

        :param uid:                 Gene id
        :param name:                Gene name
        :param extra_relationship:  Publication ids in which the entity appeared
        """
        super().__init__(uid, extra_relationship)
        self._raw_id = uid[5:]
        self._name = name
