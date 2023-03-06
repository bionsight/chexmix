from unittest.mock import Mock

from chexmix.data import MeSH
from chexmix.datasources import mesh


def test_load_mesh(mesh_XML_mock):
    MeSH.load_XML = Mock(return_value=mesh_XML_mock)
    mesh_table = mesh.load_mesh()
    assert (mesh_table['MSHD:D058729']['level'] == 4) and (mesh_table['MSHD:D050197']['level'] == 5)
