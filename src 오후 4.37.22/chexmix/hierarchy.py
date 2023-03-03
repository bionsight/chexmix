import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Set

from chexmix import types, utils

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Node:
    id: Any
    name: str
    entity: Any  # TODO: this should be entity
    parents: List["Node"] = field(default_factory=list)
    children: List["Node"] = field(default_factory=list)
    publications: Set[types.PubTator] = field(default_factory=set)
    subpublications: Set[types.PubTator] = field(default_factory=set)  # publications of descendants

    def __repr__(self):
        return (
            f"Node(id={self.id!r}, name={self.name!r}, entity={self.entity!r}, "
            f"parents=[...{len(self.parents)!r} parents], "
            f"children=[...{len(self.children)} children], "
            f"publications=[...{len(self.publications)} publications], "
            f"subpublications=[...{len(self.subpublications)} subpublications])"
        )


class Hierarchy(ABC):
    @property
    @abstractmethod
    def node_type(self):
        pass

    @property
    @abstractmethod
    def nodes(self):
        pass

    @property
    @abstractmethod
    def roots(self):
        pass

    @abstractmethod
    def get_node(self, _id):
        pass

    def get_nodes_by_name(self, name):
        return [n for n in self.nodes if n.name is not None and name in n.name]

    @abstractmethod
    def add_nodes(self, entities):
        pass

    def attach_publication(self, publ):
        mentioned_ids = set(m.entity.id for m in publ.mentions if m.entity is not None)

        for entity_id in mentioned_ids:
            try:
                node = self.get_node(entity_id)
            except KeyError:
                prefix = {types.MeSH: "MESH", types.Taxonomy: "TAXO"}[self.node_type]

                if entity_id.startswith(prefix):
                    log.warning(f"{entity_id} is not found.")
                continue
            node.publications.add(publ)

            # update subpublications for ancestor nodes
            ancestors = list(node.parents)

            while len(ancestors) > 0:
                ancestor_node = ancestors.pop()
                ancestor_node.subpublications.add(publ)
                ancestors.extend(ancestor_node.parents)

    def attach_publications(self, publs):
        for p in publs:
            self.attach_publication(p)

    def _nodes2dict(self, nodes, sort_by):
        if sort_by is not None:
            sort_key = {
                "publications": lambda n: len(n.publications),
                "subpublications": lambda n: len(n.subpublications),
                "total_publications": lambda n: len(n.publications | n.subpublications),
                "name": lambda n: n.name or n.id,
                "id": lambda n: n.id,
            }[sort_by]
            nodes = sorted(nodes, key=sort_key, reverse=True)
        ret = {}
        for n in nodes:
            node_name = f"{n.name} ({len(n.publications)}/{(len(n.publications | n.subpublications))})"
            ret[node_name] = self._nodes2dict(n.children, sort_by)
        return ret

    def to_dict(self, sort_by=None):
        return self._nodes2dict(self.roots, sort_by)


class TaxonomyHierarchy(Hierarchy):
    def __init__(self, taxs=None):
        self._tax_tbl = {}
        if taxs is not None:
            self.add_nodes(taxs)

    @property
    def node_type(self):
        return types.Taxonomy

    @staticmethod
    def ancestor_tax_ids(taxs):
        ancestor_tax_ids = set(tax_anc.id for tax in taxs for tax_anc in tax.ancestors)
        return ancestor_tax_ids - set(tax.id for tax in taxs)

    @property
    def nodes(self):
        return list(self._tax_tbl.values())

    @property
    def roots(self):
        return [n for n in self.nodes if len(n.parents) == 0]

    def get_node(self, _id):
        return self._tax_tbl[_id]

    def _add_node(self, tax):
        if tax.id in self._tax_tbl:
            raise Exception(f"duplicated id {tax.id}")
        self._tax_tbl[tax.id] = Node(tax.id, tax.name, tax)

    def _update_parents(self, node):
        ancestors = node.entity.ancestors[-1:] if len(node.entity.ancestors) > 0 else []
        for anc in ancestors:
            if self._tax_tbl[anc.id] not in node.parents:
                node.parents.append(self._tax_tbl[anc.id])

    def _update_children(self, node):
        for p in node.parents:
            if node not in p.children:
                p.children.append(node)

    def add_nodes(self, entities):
        for tax in entities:
            assert isinstance(tax, types.Taxonomy)
            self._add_node(tax)

        for tax in entities:
            node = self.get_node(tax.id)
            self._update_parents(node)
            self._update_children(node)


class MeSHHierarchy(Hierarchy):
    def __init__(self, meshs=None):
        self._mesh_tbl = {}
        self._tree_number2id = {}
        if meshs is not None:
            self.add_nodes(meshs)

    @property
    def node_type(self):
        return types.MeSH

    @staticmethod
    def ancestor_tree_numbers(tree_number):
        tokens = tree_number.split(".")
        return [".".join(tokens[:idx]) for idx in range(1, len(tokens))]

    @staticmethod
    def get_unidentified_tree_numbers(meshs):
        """
        get unidentified tree_numbers in MeSHs
        :param meshs:
        :return:
        """
        all_meshs = set(meshs) | set(heading for mesh in meshs if mesh.headings for heading in mesh.headings)

        tree_numbers = set(
            utils.flatten_list([mesh.tree_numbers for mesh in all_meshs if mesh.tree_numbers is not None])
        )
        meshs_tree_numbers = []
        for tree_number in tree_numbers:
            meshs_tree_numbers.append(MeSHHierarchy.ancestor_tree_numbers(tree_number))
        return set(utils.flatten_list(meshs_tree_numbers)) - tree_numbers

    @property
    def nodes(self):
        return list(self._mesh_tbl.values())

    @property
    def roots(self):
        return [n for n in self.nodes if len(n.parents) == 0]

    def get_node(self, _id):
        return self._mesh_tbl.get(_id) or self._mesh_tbl[self._tree_number2id[_id]]

    def _add_node(self, mesh):
        if mesh.id in self._mesh_tbl:
            return

        self._mesh_tbl[mesh.id] = Node(mesh.id, mesh.name, mesh)
        for tree_number in mesh.tree_numbers or []:
            self._tree_number2id[tree_number] = mesh.id

        if mesh.headings is not None:
            for heading in mesh.headings:
                self._add_node(heading)

    def _update_parents(self, node):
        mesh = node.entity
        if mesh.tree_numbers is not None:
            parent_tree_numbers = [
                tree_number.rsplit(".", 1)[0] for tree_number in mesh.tree_numbers if "." in tree_number
            ]
            parent_ids = set(self._tree_number2id[tree_number] for tree_number in parent_tree_numbers)
            node.parents.extend(self._mesh_tbl[parent_id] for parent_id in parent_ids)
        if mesh.headings is not None:
            node.parents.extend(self._mesh_tbl[heading.id] for heading in mesh.headings)

    def _update_children(self, node):
        for p in node.parents:
            if node not in p.children:
                p.children.append(node)

    def add_nodes(self, entities):
        for mesh in entities:
            assert isinstance(mesh, self.node_type)
            self._add_node(mesh)

        for _, node in self._mesh_tbl.items():
            self._update_parents(node)
            self._update_children(node)
