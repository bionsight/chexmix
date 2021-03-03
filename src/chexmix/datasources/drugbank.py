import io
import zipfile

import pandas as pd
import xmlschema

from chexmix.utils import first


def load_drugbank():
    db_schema = xmlschema.XMLSchema('/data_repo/mirror/drugbank/5.1.5/drugbank.xsd')
    db_zip = zipfile.ZipFile('/data_repo/mirror/drugbank/5.1.5/drugbank_all_full_database.xml.zip')
    b_io = io.BytesIO(db_zip.read('full database.xml'))
    db_xml = db_schema.to_dict(b_io)
    return db_xml


def parse_drugbank_small_molecule(drugbank_small_molecule):
    assert drugbank_small_molecule['@type'] == 'small molecule'

    record = {
        'name': drugbank_small_molecule['name'],
        'cas': drugbank_small_molecule['cas-number'],
        'id': first((db_id for db_id in drugbank_small_molecule['drugbank-id']), lambda db_id: db_id['@primary'])['$'],
        'mwt': drugbank_small_molecule.get('average-mass'),
    }

    if drugbank_small_molecule.get('calculated-properties'):
        props = {prop['kind']: prop['value'] for prop in drugbank_small_molecule['calculated-properties']['property']}
        record['smiles'] = props.get('SMILES')
        record['inchi'] = props.get('InChI')
        record['inchikey'] = props.get('InChIKey')

    return record


def get_cmpd_df(drugbank_xml):
    small_mols = [d for d in drugbank_xml['drug'] if d['@type'] == 'small molecule']
    db_df = pd.DataFrame([parse_drugbank_small_molecule(m) for m in small_mols])
    db_df = db_df[~db_df.smiles.isnull()]
    return db_df
