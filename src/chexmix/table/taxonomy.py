from typing import Dict, List

from chexmix.datasources import taxonomy
from chexmix.table.base import BaseEntity


class Taxonomy(BaseEntity):
    _TAXONOMY_TABLE = None

    @classmethod
    def taxonomy_table(cls) -> Dict:
        if cls._TAXONOMY_TABLE is None:
            cls._TAXONOMY_TABLE = taxonomy.load_taxonomy()
            for entity in cls._TAXONOMY_TABLE.values():
                entity['hierarchy'] = entity.pop('relationship')
        return cls._TAXONOMY_TABLE

    @property
    def raw_id(self) -> int:
        return self.taxonomy_table()[self.id]['raw_id']

    @property
    def name(self) -> str:
        return self.taxonomy_table()[self.id]['name']

    @property
    def rank(self) -> str:
        return self.taxonomy_table()[self.id]['rank']

    @property
    def family(self) -> str:
        return self.taxonomy_table()[self.id]['family']

    @property
    def genus(self) -> str:
        return self.taxonomy_table()[self.id]['genus']

    @property
    def level(self) -> int:
        return self.taxonomy_table()[self.id]['level']

    @property
    def lineage(self) -> List[str]:
        return self.taxonomy_table()[self.id]['lineage']

    @property
    def relationship(self) -> Dict[str, List[str]]:
        if self._relationship is None:
            self._relationship = {**self.extra_relationship, **self.taxonomy_table()[self.id]['hierarchy']}
        return self._relationship

    def __init__(self, uid: str, extra_relationship: Dict[str, List[str]]):
        """species information from Taxonomy

        :param uid:                 Taxonomy id
        :param extra_relationship:  Publication ids in which the entity appeared
        """
        super().__init__(uid, extra_relationship)
        self._relationship = None
