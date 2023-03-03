import pytest

from chexmix.datasources import mesh
from chexmix.table import MeSH


@pytest.fixture
def a_mesh(monkeypatch, mesh_table):
    def mesh_table_mock():
        return mesh_table
    monkeypatch.setattr(mesh, 'load_mesh', mesh_table_mock)
    return MeSH('MSHD:D050197', {'APPERAED_IN': ['ARTI:33989636']})


def test_mesh_table(a_mesh):
    assert a_mesh.mesh_table() == {
        'MSHC:C565928': {
            'hierarchy': {'_CONTAINS': ['MSHD:D050197', 'MSHD:D003920']},
            'id': 'MSHC:C565928', 'raw_id': 'C565928',
            'name': 'Atherosclerosis, Premature, with Deafness, Nephropathy, '
                    'Diabetes Mellitus, Photomyoclonus, and Degenerative Neurologic Disease'
        },
        'MSHD:D003920': {
            'hierarchy': {'CONTAINS': ['MSHC:C565928']},
            'id': 'MSHD:D003920', 'name': 'Diabetes Mellitus', 'raw_id': 'D003920',
            'tree_numbers': ['C18.452.394.750', 'C19.246'], 'level': 2
        },
        'MSHD:D050197': {
            'hierarchy': {'CONTAINS': ['MSHC:C565928'], 'INCLUDES': ['MSHD:D058729']},
            'id': 'MSHD:D050197', 'name': 'Atherosclerosis', 'raw_id': 'D050197',
            'tree_numbers': ['C14.907.137.126.307'], 'level': 5
        },
        'MSHD:D058729': {
            'hierarchy': {'_INCLUDES': ['MSHD:D050197']},
            'id': 'MSHD:D058729', 'name': 'Peripheral Arterial Disease', 'raw_id': 'D058729',
            'tree_numbers': ['C14.907.137.126.307.500', 'C14.907.617.671'], 'level': 4
        }
    }


def test_raw_id(a_mesh):
    assert a_mesh.raw_id == 'D050197'


def test_name(a_mesh):
    assert a_mesh.name == 'Atherosclerosis'


def test_relationship(a_mesh):
    assert a_mesh.relationship == {
        'APPERAED_IN': ['ARTI:33989636'], 'CONTAINS': ['MSHC:C565928'],
        'INCLUDES': ['MSHD:D058729']}


def test_tree_numbers(a_mesh):
    assert a_mesh.tree_numbers == ['C14.907.137.126.307']


def test_level(a_mesh):
    assert a_mesh.level == 5


def test_is_exist(a_mesh):
    assert a_mesh.is_exist('MSHD:D003920')
    assert not a_mesh.is_exist('MSHD:D006859')


def test_is_descriptor(a_mesh):
    assert a_mesh.is_descriptor('MSHD:D058729')
    assert not a_mesh.is_descriptor('MSHC:C565928')


def test_is_disease(a_mesh):
    assert a_mesh.is_disease
