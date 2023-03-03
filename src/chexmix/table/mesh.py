from typing import Dict, List, Union

from chexmix.datasources import mesh
from chexmix.table.base import BaseEntity


class MeSH(BaseEntity):
    _mesh_table = None

    @classmethod
    def mesh_table(cls) -> Dict[str, Union[str, List[str], List[Dict]]]:
        if cls._mesh_table is None:
            cls._mesh_table = mesh.load_mesh()
            for entity in cls._mesh_table.values():
                entity['hierarchy'] = entity.pop('relationship')
        return cls._mesh_table

    @property
    def raw_id(self) -> str:
        return self.mesh_table()[self.id]['raw_id']

    @property
    def name(self) -> str:
        return self.mesh_table()[self.id]['name']

    @property
    def relationship(self) -> Dict[str, List[str]]:
        if self._relationship is None:
            self._relationship = {**self.extra_relationship, **self.mesh_table()[self.id]['hierarchy']}
        return self._relationship

    @property
    def tree_numbers(self) -> List[str]:
        return self.mesh_table()[self.id]['tree_numbers'] if self.id[3] == 'D' else []

    @property
    def level(self) -> int:
        return self.mesh_table()[self.id]['level'] if self.id[3] == 'D' else 0

    def __init__(self, uid: str, extra_relationship: Dict[str, List[str]]):
        """Chemical, Disease information from MeSH

        :param uid:                 MeSH id
        :param extra_relationship:  Publication ids in which the entity appeared
        """
        super().__init__(uid, extra_relationship)
        self._relationship = None

    @staticmethod
    def is_exist(bio_id: str) -> bool:
        return bio_id in MeSH.mesh_table().keys()

    @staticmethod
    def is_descriptor(uid: str) -> bool:
        return uid[:4] == 'MSHD'

    @staticmethod
    def is_MeSH(bio_id: str) -> bool:
        return bio_id[:3] == 'MSH'

    def is_disease(self) -> bool:
        if self.is_descriptor(self.id):
            tree_numbers = self.tree_numbers
        else:
            tree_numbers = [
                tree_number
                for mesh_id in self.relationship['_CONTAINS']
                if self.is_descriptor(mesh_id)
                for tree_number in self.mesh_table()[mesh_id]['tree_numbers']
            ]
        for tree_number in tree_numbers:
            if tree_number[0] in ['C', 'F']:
                return True
        return False
