import pandas as pd
from chembl_webresource_client.new_client import new_client


def similarity_search(smiles, similarity):
    cmpds = new_client.similarity.filter(smiles=smiles, similarity=similarity)
    props = [cmpd['molecule_properties'] for cmpd in cmpds]
    structs = [cmpd['molecule_structures'] for cmpd in cmpds]

    cmpd_df = pd.concat([pd.DataFrame(cmpds), pd.DataFrame(props), pd.DataFrame(structs)], axis=1)
    cmpd_df['similarity'] = cmpd_df.similarity.astype(float) / 100.0
    cmpd_df = cmpd_df.drop(columns=['molecule_properties', 'molecule_structures', 'molfile'])\
                     .rename(columns={'molecule_chembl_id': 'id'}).copy()
    return cmpd_df


def get_activity_df(chembl_ids, chunk_size=50):
    activities = []
    for idx in range(0, len(chembl_ids), chunk_size):
        activities += new_client.activity.filter(molecule_chembl_id__in=chembl_ids[idx: idx + chunk_size])
    return pd.DataFrame(activities)
