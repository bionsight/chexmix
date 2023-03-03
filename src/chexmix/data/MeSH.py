import logging
import os

from lxml import etree

import chexmix.utils as utils
from chexmix.env import data_path

logger = logging.getLogger(__name__)

MESH_XML_PATH = os.path.join(data_path, 'mesh/MESH_FILES/xmlmesh')
MESH_DTD_PATH = os.path.join(data_path, 'mesh/dtd')

DTD_FILE_NAMES = [
    # unnecessary as nlmsupplementalrecordset imports this file
    # 'nlmdescriptorrecordset_20190101.dtd',
    'nlmqualifierrecordset_20190101.dtd',
    'nlmsupplementalrecordset_20190101.dtd']

DTD_FILE_LIST = [os.path.join(MESH_DTD_PATH, filename)
                 for filename in DTD_FILE_NAMES]

XML_FILE_TABLE = {'descriptor': 'desc2020.xml',
                  'qualifier': 'qual2020.xml',
                  'supplement': 'supp2020.xml'}
XML_FILE_TABLE = {k: os.path.join(MESH_XML_PATH, filename)
                  for k, filename in XML_FILE_TABLE.items()}

DESC_XML_PATH = os.path.join(MESH_XML_PATH, 'desc2019.xml')


def get_DTD_list():
    """return DTD list. One can validate XML using this."""
    return [etree.DTD(f) for f in DTD_FILE_LIST]


def get_MeSH_tags(network=False):
    """get the map specifying content types of tags

    Lists:
    AllowableQualifiersList, EntryCombinationList, PreviousIndexingList, SeeRelatedList,
    TreeNumberList, ConceptList, ConceptRelationList, PharmacologicalActionList,
    RelatedRegistryNumberList, TermList, ThesaurusIDlist

    Scalars:
    Annotation, ConsiderAlso, Day, DescriptorUI, HistoryNote, Month, NLMClassificationNumber,
    OnlineNote, PublicMeSHNote, PreviousIndexing, QualifierUI, Year, TreeNumber, ConceptUI,
    Concept1UI, Concept2UI, CASN1Name, RegistryNumber, RelatedRegistryNumber, ScopeNote,
    TranslatorsEnglishScopeNote, TranslatorsScopeNote, TermUI, String, Abbreviation,
    SortVersion, EntryVersion

    Entities with attributes:
    Concept, ConceptRelation, Term

    """
    if not network:
        scalar_tags = {'Abbreviation',
                       'Annotation',
                       'CASN1Name',
                       'Concept1UI',
                       'Concept2UI',
                       'ConceptUI',
                       'ConsiderAlso',
                       'Day',
                       'DescriptorUI',
                       'EntryVersion',
                       'Frequency',
                       'HistoryNote',
                       'Month',
                       'NLMClassificationNumber',
                       'Note',
                       'OnlineNote',
                       'PreviousIndexing',
                       'PublicMeSHNote',
                       'QualifierUI',
                       'RegistryNumber',
                       'RelatedRegistryNumber',
                       'ScopeNote',
                       'SortVersion',
                       'Source',
                       'String',
                       'SupplementalRecordUI',
                       'TermNote',
                       'TermUI',
                       'ThesaurusID',
                       'TranslatorsEnglishScopeNote',
                       'TranslatorsScopeNote',
                       'TreeNumber',
                       'Year'}

        list_tags = {'AllowableQualifiersList',
                     'ConceptList',
                     'ConceptRelationList',
                     'DescriptorRecordSet',
                     'EntryCombinationList',
                     'HeadingMappedToList',
                     'IndexingInformationList',
                     'PharmacologicalActionList',
                     'PreviousIndexingList',
                     'QualifierRecordSet',
                     'RelatedRegistryNumberList',
                     'SeeRelatedList',
                     'SourceList',
                     'SupplementalRecordSet',
                     'TermList',
                     'ThesaurusIDlist',
                     'TreeNumberList'}

        map_tags = {'AllowableQualifier',
                    'ChemicalReferredTo',
                    'Concept',
                    'ConceptName',
                    'ConceptRelation',
                    'DateCreated',
                    'DateEstablished',
                    'DateRevised',
                    'DescriptorName',
                    'DescriptorRecord',
                    'DescriptorReferredTo',
                    'ECIN',
                    'ECOUT',
                    'EntryCombination',
                    'HeadingMappedTo',
                    'IndexingInformation',
                    'PharmacologicalAction',
                    'QualifierName',
                    'QualifierRecord',
                    'QualifierReferredTo',
                    'SeeRelatedDescriptor',
                    'SupplementalRecord',
                    'SupplementalRecordName',
                    'Term'}

    else:
        dtd_list = get_DTD_list()
        elms = utils.flatten_list([dtd.elements() for dtd in dtd_list])
        list_tags = [e.name for e in elms if ((e.type == 'element') and
                                              (e.content.type == 'element') and
                                              ((e.content.occur == 'mult') or (e.content.occur == 'plus')))]
        scalar_tags = [e.name for e in elms if (e.type == 'mixed')]

        map_tags = [e.name for e in elms if e.name not in scalar_tags and e.name not in list_tags]

    node_types_ = {'scalar': set(scalar_tags),
                   'list': set(list_tags),
                   'map': set(map_tags)}
    return node_types_


node_types = get_MeSH_tags()


def get_node_type(node):
    for k, node_set in node_types.items():
        if node.tag in node_set:
            return k

    return None


def parse_date(node):
    date_keys = ['Year', 'Month', 'Day']
    date_tuple = ['YYYY', 'MM', 'DD']

    for x in node:
        idx = date_keys.index(x.tag)
        if idx >= 0:
            date_tuple[idx] = x.text
        else:
            raise Exception(x.tag)
    return ''.join(date_tuple)


def normalize_(node):
    """
    get a string if node is scalar, a map if map, a list if list.
    Note there are some exceptions for names, and dates.
    """
    node_type = get_node_type(node)

    if node.tag in {'DateCreated', 'DateRevised', 'DateEstablished'}:
        # convert {"Year": "YYYY", "Month": "MM", "Day": "DD"} to "YYYYMMDD"
        return parse_date(node)
    elif node.tag in {'DescriptorName', 'QualifierName', 'ConceptName', 'SupplementalRecordName'}:
        # ignore unnecessary nested "String"
        return node[0].text
    elif node_type == 'map':
        m = dict(node.attrib)
        for elm in node:
            if elm.tag in m:
                Exception('Duplicated field', node, elm)
            m[elm.tag] = normalize_(elm)
        return m
    elif node_type == 'scalar':
        return node.text
    elif node_type == 'list':
        return [normalize_(elm) for elm in node]

    raise Exception('Unknown node type', node, node_type)


def postprocess_descriptor_(descriptor):
    """
    for convenience of indexing descriptor:
    - add AllowableQualifiersListForIndex with QualifierUIs only
    - add PharmacologicalActionListForIndex with DescriptorUIs

    note this mutates the original dict.
    """
    if 'AllowableQualifiersList' in descriptor:
        descriptor['AllowableQualifiersListForIndex'] = [qual['QualifierReferredTo']['QualifierUI']
                                                         for qual in descriptor['AllowableQualifiersList']]

    if 'PharmacologicalActionList' in descriptor:
        descriptor['PharmacologicalActionListForIndex'] = [desc['DescriptorReferredTo']['DescriptorUI']
                                                           for desc in descriptor['PharmacologicalActionList']]

    return descriptor


def _trim_head_star(name):
    if name[0] == '*':
        return name[1:]
    return name


def get_UI_from_IndexingInformation(indexing_info):
    if 'DescriptorReferredTo' in indexing_info:
        return indexing_info['DescriptorReferredTo']['DescriptorUI']
    elif 'QualifierReferredTo' in indexing_info:
        return indexing_info['QualifierReferredTo']['QualifierUI']
    elif 'ChemicalReferredTo' in indexing_info:
        return indexing_info['ChemicalReferredTo']['SupplementalRecordUI']

    raise ValueError('unknown index information', indexing_info)


def postprocess_supplement_(supplement):
    """
    - add HeadingMappedToListForIndex with stripped DescriptorUI, i.e., not '*' at the head
    - add IndexingInformationListForIndex with DescriptorUIs

    note this mutates the original dict.
    """
    if 'HeadingMappedToList' in supplement:
        supplement['HeadingMappedToListForIndex'] = [_trim_head_star(supp['DescriptorReferredTo']['DescriptorUI'])
                                                     for supp in supplement['HeadingMappedToList']]

    if 'IndexingInformationList' in supplement:
        supplement['IndexingInformationListForIndex'] = [_trim_head_star(get_UI_from_IndexingInformation(indexing_info))
                                                         for indexing_info in supplement['IndexingInformationList']]

    return supplement


POSTPROCESSOR_TABLE = {'descriptor': postprocess_descriptor_,
                       'qualifier': None,
                       'supplement': postprocess_supplement_}


def load_XML():
    """
    return MeSHs grouped by type,
    i.e., {'descriptor': [descriptor MeSH ...],
           'qualifier': [qualifier MeSH ...],
           'supplement': [supplement MeSH ...],}
    """
    m = {}
    for col, xml_file in XML_FILE_TABLE.items():
        with open(xml_file, "r") as f:
            logger.info(f'load {xml_file}')
            mesh_list = normalize_(etree.parse(f).getroot())
            postprocessor = POSTPROCESSOR_TABLE[col]

            if postprocessor:
                mesh_list = [postprocessor(mesh) for mesh in mesh_list]

            m[col] = mesh_list

    return m


def load(col_name):
    """return MeSHs for a given column name"""
    with open(XML_FILE_TABLE[col_name], "r") as f:
        logger.info(f'load {XML_FILE_TABLE[col_name]}')
        mesh_list = normalize_(etree.parse(f).getroot())
        postprocessor = POSTPROCESSOR_TABLE[col_name]

        if postprocessor:
            mesh_list = [postprocessor(mesh) for mesh in mesh_list]
        return mesh_list


################################################################################
#
# Postprocess to generate relation table


def __get_TU_map(MeSH_list, on):
    """
    Construct a map: TreeNumber -> Unique Id (UI)
    """
    return {tn: m[on] for m in MeSH_list for tn in m.get('TreeNumberList', [])}


def __get_parent_tree_number(tree_number):
    idx = tree_number.rfind('.')
    if idx < 0:
        return None
    return tree_number[:idx]


def __flatten_TreeNumbers(MeSH_list, on):
    return [(m[on], __get_parent_tree_number(tn)) for m in MeSH_list for tn in m.get('TreeNumberList', [])]


def __get_IS_A_tuples(MeSH_list, on, kind):
    TU_map = __get_TU_map(MeSH_list, on)

    IS_A_tuples = __flatten_TreeNumbers(MeSH_list, on)

    # remove roots in the hierarchy
    IS_A_tuples = [(s, e) for s, e in IS_A_tuples if e]
    IS_A_tuples = [(s, TU_map[e], kind) for s, e in IS_A_tuples]

    return IS_A_tuples


def get_IS_A_tuples(MeSH_table):
    """
    return a list of relation tuples of IS_A from TreeNumber, i.e. hierarchy
    """

    IS_A_tuples = \
        __get_IS_A_tuples(MeSH_table['descriptor'], 'DescriptorUI', 'Descriptor') + \
        __get_IS_A_tuples(MeSH_table['qualifier'], 'QualifierUI', 'Qualifier')

    return IS_A_tuples


def __flatten_relations(MeSH_list, on, list_key, kind=None):
    return [(m[on], ui, kind) for m in MeSH_list for ui in m.get(list_key, [])]


def get_relation_table(MeSH_table):
    ret = {'HAS_PHARMA_ACTION': __flatten_relations(MeSH_table['descriptor'],
                                                    'DescriptorUI',
                                                    'PharmacologicalActionListForIndex'),
           'QUALIFIED_AS': __flatten_relations(MeSH_table['descriptor'],
                                               'DescriptorUI',
                                               'AllowableQualifiersListForIndex'),
           'IS_A': __flatten_relations(MeSH_table['supplement'],
                                       'SupplementalRecordUI',
                                       'HeadingMappedToListForIndex',
                                       'Supplement'),
           'RELATED_TO': __flatten_relations(MeSH_table['supplement'],
                                             'SupplementalRecordUI',
                                             'IndexingInformationListForIndex')}
    ret['IS_A'] = ret['IS_A'] + get_IS_A_tuples(MeSH_table)

    return ret
