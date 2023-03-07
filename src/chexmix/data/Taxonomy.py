import os
import zipfile
from typing import Dict, IO, List, Union
import pandas as pd

from chexmix import utils
from chexmix.env import data_path

TAXONOMY_PATH = os.path.join(data_path, 'taxonomy/new_taxdump')
ZIP_FILE = os.path.join(TAXONOMY_PATH, 'new_taxdump.zip')


def read_csv_(file_name_or_buf: Union[str, IO], col_names: List[str]) -> pd.DataFrame:
    return pd.read_csv(
        file_name_or_buf,
        sep='|',
        header=None,
        index_col=False,
        names=col_names,
        converters={name: utils.strip for name in col_names},
    )


def read_taxonomy_(zfile: IO) -> Dict[str, pd.DataFrame]:
    """
    The followings are taxonomy related files and their contents:

    nodes.dmp
    ---------
        tax_id					-- node id in GenBank taxonomy database
        parent tax_id				-- parent node id in GenBank taxonomy database
        rank					-- rank of this node (superkingdom, kingdom, ...)
        embl code				-- locus-name prefix; not unique
        division id				-- see division.dmp file
        inherited div flag  (1 or 0)		-- 1 if node inherits division from parent
        genetic code id				-- see gencode.dmp file
        inherited GC  flag  (1 or 0)		-- 1 if node inherits genetic code from parent
        mitochondrial genetic code id		-- see gencode.dmp file
        inherited MGC flag  (1 or 0)		-- 1 if node inherits mitochondrial gencode from parent
        GenBank hidden flag (1 or 0)            -- 1 if name is suppressed in GenBank entry lineage
        hidden subtree root flag (1 or 0)       -- 1 if this subtree has no sequence data yet
        comments				-- free-text comments and citations
        plastid genetic code id                 -- see gencode.dmp file
        inherited PGC flag  (1 or 0)            -- 1 if node inherits plastid gencode from parent
        specified_species			-- 1 if species in the node's lineage has formal name
        hydrogenosome genetic code id           -- see gencode.dmp file
        inherited HGC flag  (1 or 0)            -- 1 if node inherits hydrogenosome gencode from parent

    names.dmp
    ---------
        tax_id					-- the id of node associated with this name
        name_txt				-- name itself
        unique name				-- the unique variant of this name if name not unique
        name class				-- (synonym, common name, ...)


    gencode.dmp
    -----------
        genetic code id				-- GenBank genetic code id
        abbreviation				-- genetic code name abbreviation
        name					-- genetic code name
        cde					-- translation table for this genetic code
        starts					-- start codons for this genetic code

    rankedlineage.dmp
    -----------------
        tax_id                                  -- node id
        tax_name                                -- scientific name of the organism
        species                                 -- name of a species (coincide with organism name for species-level
                                                                      nodes)
        genus					-- genus name when available
        family					-- family name when available
        order					-- order name when available
        class					-- class name when available
        phylum					-- phylum name when available
        kingdom					-- kingdom name when available
        superkingdom				-- superkingdom (domain) name when available

    taxidlineage.dmp
    ----------------
        tax_id                                  -- node id
        lineage                                 -- sequence of node ids separated by space denoting nodes' ancestors
                                                   starting from the most distant one and ending with the immediate one

    """

    content_column_table = {
        'nodes.dmp': [
            'tax_id',
            'parent_tax_id',
            'rank',
            'embl_code',
            'div',
            'div_flag',
            'GC',
            'inherited_GC_flag',
            'MGC',
            'inherited_MGC_flag',
            'genbank_hidden',
            'hidden_subtree',
            'comments',
            'plastid',
            'PGC_flag',
            'specified_species',
            'HGC',
            'HGC_flag',
        ],
        'names.dmp': ['tax_id', 'name_txt', 'unique_name', 'name_class'],
        'gencode.dmp': ['GC', 'abbr', 'name', 'cde', 'starts'],
        'rankedlineage.dmp': [
            'tax_id',
            'tax_name',
            'species',
            'genus',
            'family',
            'order',
            'class',
            'phylum',
            'kingdom',
            'superkingdom',
        ],
        'taxidlineage.dmp': ['tax_id', 'lineage'],
    }

    content_table = {
        filename: read_csv_(zfile.open(filename), col_names) for filename, col_names in content_column_table.items()
    }

    return content_table


def merge_dfs(dfs: List[pd.DataFrame], on: str, how: str = 'inner') -> pd.DataFrame:
    ret_df = dfs[0]
    for df in dfs[1:]:
        ret_df = ret_df.merge(df, on=on, how=how)

    return ret_df


def normalize_tax(tax) -> Dict[str, int]:
    """normalize taxonomy data"""
    tax = utils.remove_none_vals(tax)
    tax_keys = [
        'tax_id',
        'parent_tax_id',
        'div',
        'div_flag',
        'GC',
        'inherited_GC_flag',
        'MGC',
        'inherited_MGC_flag',
        'genbank_hidden',
        'hidden_subtree',
        'specified_species',
    ]
    tax = {k: int(v) if k in tax_keys else v for k, v in tax.items()}
    tax['lineage'] = [int(token) for token in tax['lineage'].split()]

    return tax


def normalize_gc(gc: Dict) -> Dict:
    """normalize gencode data"""

    gc['GC'] = int(gc['GC'])

    return gc


################################################################################
# Public


def load_taxdump() -> Dict[str, List[dict]]:
    """
    returns {'taxonomy': taxonomy_table, 'gencode': gencode_table}, where
    the tables are lists of dict.
    """

    with zipfile.ZipFile(ZIP_FILE, 'r') as zfile:
        content_table = read_taxonomy_(zfile)
        taxonomy_table = merge_dfs(
            [content_table[x] for x in ['nodes.dmp', 'rankedlineage.dmp', 'taxidlineage.dmp']]
            + [content_table['names.dmp'].groupby('tax_id')['name_txt'].apply(','.join).reset_index()],
            on='tax_id',
        ).to_dict('records')
        taxonomy_table = [normalize_tax(tax) for tax in taxonomy_table]
        gencode_table = [normalize_gc(gc) for gc in content_table['gencode.dmp'].to_dict('records')]
        return {'taxonomy': taxonomy_table, 'gencode': gencode_table}  # 'raw': content_table,
