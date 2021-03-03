from collections import namedtuple
from typing import List, NamedTuple

ChEMBLCompound = namedtuple("ChEMBLCompound", [
    "pref_name",
    "chembl_id",
    "molregno",
    "can_smiles",
    "smiles",
    "inchi",
    "inchikey",
    "rdmol",
])

PubChemCompound = namedtuple("PubChemCompound", [
    'cid',
    'rdmol',
    'cactvs_complexity',
    'hbond_acceptor',
    'hbond_doner',
    'rotable_bond',
    'inchi',
    'inchikey',
    'mwt',
    'total_charge',
    'can_smiles',
    'iso_smiles',
    'smiles',
    'cas',
], defaults=(None,))

ZINCCompound = namedtuple("ZINCCompound", [
    'smiles',
    'zinc_id',
    'inchikey',
    'mwt',
    'logp',
    'reactive',
    'purchasable',
    'tranche_name',
    'features',
    'rdmol',
])

AllChemMeta = namedtuple("AllChemMeta", [
    'source',
    'id',
    'tags',
    'hbond_acceptor',
    'hbond_doner',
    'rotable_bond',
    'ring_count',
    'inchikey',
    'mwt',
    'logp',
    'm4l2048',
    'm4l2048_count',
])


class PubTator(NamedTuple):
    id: str
    title: str
    abstract: str
    mentions: list

    def __hash__(self):
        return hash(self.id) * hash(self.title) * hash(self.abstract)


Mention = namedtuple("Mention", [
    'begin',
    'end',
    'text',
    'type',
    'entity',
])

Entity = namedtuple("Entity", [
    'id',
    'name',
    'type',
])

Taxonomy = namedtuple("Taxonomy", [
    'id',
    'name',
    'type',
    'ancestors',
])


class MeSH(NamedTuple):
    id: str
    name: str
    type: str
    tree_numbers: List[str]
    headings: List['MeSH']

    def __hash__(self):
        return hash(self.id) * hash(self.name)


KeggCompound = namedtuple("KeggCompound", [
    'entry',
    'name',
    'formula',
    'mass',
    'pathway',
    'enzyme',
    'structures',
    'dblinks',
])

KeggEnzyme = namedtuple("KeggEnzyme", [
    'entry',
    'name',
    'classname',
    'sysname',
    'reaction',
    'substrate',
    'product',
    'inhibitor',
    'cofactor',
    'effector',
    'comment',
    'pathway',
    'genes',
    'disease',
    'structures',
    'dblinks',
])

KeggGene = namedtuple("KeggGene", [
    'entry',
    'name',
    'definition',
    'orthology',
    'organism',
    'position',
    'motif',
    'dblinks',
])

EntrezPubMed = namedtuple("EntrezPubMed", [
    'pmid',
    'title',
    'abstract',
    'completed_date',
    'revised_date',
])
