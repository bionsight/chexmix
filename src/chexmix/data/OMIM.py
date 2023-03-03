import logging
import os
from typing import Dict, List

import pandas as pd

from chexmix.env import data_path

logger = logging.getLogger(__name__)
OMIM_PATH = os.path.join(data_path, 'omim')


def load_genemap2() -> List[dict]:
    logger.info('load genemap2')
    file_path = os.path.join(OMIM_PATH, 'genemap2.txt')
    names = [
        'Chromosome',
        'Genomic Position Start',
        'Genomic Position End',
        'Cyto Location',
        'Computed Cyto Location',
        'Mim Number',
        'Gene Symbols',
        'Gene Name',
        'Approved Symbol',
        'Entrez Gene ID',
        'Ensembl Gene ID',
        'Comments',
        'Phenotypes',
        'Mouse Gene Symbol/ID',
    ]
    df_genemap2 = pd.read_csv(file_path, sep='\t', skiprows=4, skipfooter=63, engine='python', names=names)

    df_genemap2['Mouse Gene Symbol'] = df_genemap2['Mouse Gene Symbol/ID'].apply(
        lambda x: x.split()[0] if isinstance(x, str) else None
    )
    df_genemap2['Mouse Gene ID'] = df_genemap2['Mouse Gene Symbol/ID'].apply(
        lambda x: x.split()[1] if isinstance(x, str) else None
    )
    df_genemap2 = df_genemap2.drop('Mouse Gene Symbol/ID', axis=1)

    gm2_records = df_genemap2.to_dict('records')
    gm2_records = [
        {k: (v if not isinstance(v, float) else int(v)) for k, v in row.items() if not pd.isnull(v)}
        for row in gm2_records
    ]
    return gm2_records


def load_mim_titles() -> List[dict]:
    logger.info('load mimTitles')
    file_path = os.path.join(OMIM_PATH, 'mimTitles.txt')
    names = ['Prefix', 'Mim Number', 'Preferred Title', 'Alternative Title', 'Included Title']
    df_mim_titles = pd.read_csv(file_path, sep='\t', skiprows=3, skipfooter=13, engine='python', names=names)
    min_title_cols = ['Preferred Title', 'Alternative Title', 'Included Title']
    df_mim_titles['Title'] = df_mim_titles.apply(
        lambda r: '; '.join([r[col] for col in min_title_cols if not pd.isnull(r[col])]),
        axis=1,
    )
    mt_records = df_mim_titles.to_dict('records')
    mt_records = [
        {k: (v if not isinstance(v, float) else int(v)) for k, v in row.items() if not pd.isnull(v)}
        for row in mt_records
    ]
    return mt_records


def load_morbidmap() -> List[dict]:
    logger.info('load morbidmap')
    file_path = (os.path.join(OMIM_PATH, 'morbidmap.txt'),)
    names = ['Phenotype', 'Gene Symbols', 'MIM Number', 'Cyto Location']
    df_morbidmap = pd.read_csv(file_path, sep='\t', skiprows=4, skipfooter=24, engine='python', names=names)
    mm_records = df_morbidmap.to_dict('records')
    mm_records = [
        {k: (v if not isinstance(v, float) else int(v)) for k, v in row.items() if not pd.isnull(v)}
        for row in mm_records
    ]
    return mm_records


def load_mim2gene() -> Dict:
    logger.info('load mim2gene')
    file_path = os.path.join(OMIM_PATH, 'mim2gene.txt')
    names = ['MIM Number', 'MIM Entry Type', 'Entrez Gene ID', 'Approved Gene Symbol', 'Ensembl Gene ID']
    df_mim2gene = pd.read_csv(file_path, sep='\t', skiprows=5, engine='python', names=names)
    m2g_records = df_mim2gene.to_dict('records')
    m2g_records = [
        {k: (v if not isinstance(v, float) else int(v)) for k, v in row.items() if not pd.isnull(v)}
        for row in m2g_records
    ]

    return m2g_records


def load_omim() -> Dict:
    data_map = {
        'genemap2': load_genemap2(),
        'mimTitles': load_mim_titles(),
        'morbidmap': load_morbidmap(),
        'MIM2gene': load_mim2gene(),
    }

    omim_id2mim = {m['Mim Number']: m for m in data_map['mimTitles']}

    for dataset_name in ['genemap2', 'morbidmap', 'MIM2gene']:
        logger.info("add", dataset_name)
        for m in data_map[dataset_name]:
            m_id = m.get('Mim Number') or m['MIM Number']
            if m_id in omim_id2mim:
                omim_id2mim[m_id].update(m)
            else:
                logger.error("not found", m_id)
    data_map['omim'] = omim_id2mim.values()

    return data_map
