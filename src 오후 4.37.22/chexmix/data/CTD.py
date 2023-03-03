import logging
import os
from typing import List, Optional

import pandas as pd
from chexmix.env import data_path

logger = logging.getLogger(__name__)
CTD_PATH = os.path.join(data_path, 'ctd')
SKIP_ROW_TABLE = {'interaction_types': 26, 'exposure': 28, 'bioentity': 29}


def df2records(df: pd.DataFrame, float_col: Optional[List] = None) -> List[dict]:
    float_col = float_col or []
    records = df.to_dict('records')
    return [
        {
            k: (v if (not isinstance(v, float) or (k in float_col)) else int(v))
            for k, v in row.items()
            if not pd.isnull(v)
        }
        for row in records
    ]


def load_chemical_gene_interaction() -> List[dict]:
    logger.info('load chemical gene interaction')
    file_path = os.path.join(CTD_PATH, 'CTD_chem_gene_ixns.tsv.gz')
    names = [
        'ChemicalName',
        'ChemicalID',
        'CasRN',
        'GeneSymbol',
        'GeneID',
        'GeneForms',
        'Organism',
        'OrganismID',
        'Interaction',
        'InteractionActions',
        'PubMedIDs',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df)


def load_chemical_gene_interaction_types() -> List[dict]:
    logger.info('load chemical gene interaction types')
    file_path = os.path.join(CTD_PATH, 'CTD_chem_gene_ixn_types.tsv')
    names = ['TypeName', 'Code', 'Description', 'ParentCode']
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['interaction_types'], names=names)

    return df2records(df)


def load_chemical_disease_associations() -> List[dict]:
    logger.info('load chemical disease associations')
    file_path = os.path.join(CTD_PATH, 'CTD_chemicals_diseases.tsv.gz')
    names = [
        'ChemicalName',
        'ChemicalID',
        'CasRN',
        'DiseaseName',
        'DiseaseID',
        'DirectEvidence',
        'InferenceGeneSymbol',
        'InferenceScore',
        'OmimIDs',
        'PubMedIDs',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df, ['InferenceScore'])


def load_chemical_go_associations() -> List[dict]:
    logger.info('load chemical go associations')
    file_path = os.path.join(CTD_PATH, 'CTD_chem_go_enriched.tsv.gz')
    names = [
        'ChemicalName',
        'ChemicalID',
        'CasRN',
        'Ontology',
        'GOTermName',
        'GOTermID',
        'HighestGOLevel',
        'PValue',
        'CorrectedPValue',
        'TargetMatchQty',
        'TargetTotalQty',
        'BackgroundMatchQty',
        'BackgroundTotalQty',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df, ['PValue', 'CorrectedPValue'])


def load_chemical_pathway_associations() -> List[dict]:
    logger.info('load chemical pathway associations')
    file_path = os.path.join(CTD_PATH, 'CTD_chem_pathways_enriched.tsv.gz')
    names = [
        'ChemicalName',
        'ChemicalID',
        'CasRN',
        'PathwayName',
        'PathwayID',
        'PValue',
        'CorrectedPValue',
        'TargetMatchQty',
        'TargetTotalQty',
        'BackgroundMatchQty',
        'BackgroundTotalQty',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)
    return df2records(df, ['PValue', 'CorrectedPValue'])  # nan


def load_gene_disease_associations() -> List[dict]:
    logger.info('load gene disease associations')
    file_path = os.path.join(CTD_PATH, 'CTD_genes_diseases.tsv.gz')
    names = [
        'GeneSymbol',
        'GeneID',
        'DiseaseName',
        'DiseaseID',
        'DirectEvidence',
        'InferenceChemicalName',
        'InferenceScore',
        'OmimIDs',
        'PubMedID',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df, ['InferenceScore'])


def load_gene_pathway_associations() -> List[dict]:
    logger.info('load gene pathway associations')
    file_path = os.path.join(CTD_PATH, 'CTD_genes_pathways.tsv.gz')
    names = ['GeneSymbol', 'GeneID', 'PathwayName', 'PathwayID']
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)
    return df2records(df)


def load_disease_pathway_associations() -> List[dict]:
    logger.info('load disease pathway associations')
    file_path = os.path.join(CTD_PATH, 'CTD_diseases_pathways.tsv.gz')
    names = ['DiseaseName', 'DiseaseID', 'PathwayName', 'PathwayID', 'InferenceGeneSymbol']
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df)


def load_chem_pheno_interactions() -> List[dict]:
    logger.info('load chem phenotype interactions')
    file_path = os.path.join(CTD_PATH, 'CTD_pheno_term_ixns.tsv.gz')
    names = [
        'ChemicalName',
        'ChemicalID',
        'CasRN',
        'PhenotypeName',
        'PhenotypeID',
        'ComentionedTerms',
        'Organism',
        'OrganismID',
        'Interaction',
        'InteractionActions',
        'AnatomyTerms',
        'InferenceGeneSymbols',
        'PubMedIDs',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df)


def load_exposure_study_associations() -> List[dict]:
    logger.info('load exposure study interactions')
    file_path = os.path.join(CTD_PATH, 'CTD_exposure_studies.tsv.gz')
    names = [
        'Reference',
        'StudyFactors',
        'ExposureStressors',
        'Receptors',
        'StudyCountries',
        'Mediums',
        'ExposureMarkers',
        'Diseases',
        'Phenotypes',
        'AuthorSummary',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['exposure'], names=names)

    return df2records(df)


def load_exposure_event_associations() -> List[dict]:
    logger.info('load exposure event interactions')
    file_path = os.path.join(CTD_PATH, 'CTD_exposure_events.tsv.gz')
    names = [
        'ExposureStressorName',
        'ExposureStressorID',
        'StressorSourceCategory',
        'StressorSourceDetails',
        'NumberOfStressorSamples',
        'StressorNotes',
        'NumberOfReceptors',
        'Receptors',
        'ReceptorNotes',
        'SmokingStatus',
        'Age',
        'AgeUnitsOfMeasurement',
        'AgeQualifier',
        'Sex',
        'Race',
        'Methods',
        'DetectionLimit',
        'DetectionLimitUOM',
        'DetectionFrequency',
        'Medium',
        'ExposureMarker',
        'ExposureMarkerID',
        'MarkerLevel',
        'MarkerUnitsOfMeasurement',
        'MarkerMeasurementStatistic',
        'AssayNotes',
        'StudyCountries',
        'StateOrProvince',
        'CityTownRegionArea',
        'ExposureEventNotes',
        'OutcomeRelationship',
        'DiseaseName',
        'DiseaseID',
        'PhenotypeName',
        'PhenotypeID',
        'PhenotypeActionDegreeTypeAnatomy',
        'ExposureOutcomeNotes',
        'Reference',
        'AssociatedStudyTitles',
        'EnrollmentStartYear',
        'EnrollmentEndYear',
        'StudyFactors',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['exposure'], names=names)

    return df2records(df)


def load_pheno_disease_bioprocess_associations() -> List[dict]:
    logger.info('load pheno disease bio-process')
    file_path = os.path.join(CTD_PATH, 'CTD_Phenotype-Disease_biological_process_associations.tsv.gz')
    names = [
        'GOName',
        'GOID',
        'DiseaseName',
        'DiseaseID',
        'InferenceChemicalQty',
        'InferenceChemicalNames',
        'InferenceGeneQty',
        'InferenceGeneSymbols',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df)


def load_pheno_disease_cellcomp_associations() -> List[dict]:
    logger.info('load pheno disease cellular-component')
    file_path = os.path.join(CTD_PATH, 'CTD_Phenotype-Disease_cellular_component_associations.tsv.gz')
    names = [
        'GOName',
        'GOID',
        'DiseaseName',
        'DiseaseID',
        'InferenceChemicalQty',
        'InferenceChemicalNames',
        'InferenceGeneQty',
        'InferenceGeneSymbols',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df)


def load_pheno_disease_mole_fn_associations() -> List[dict]:
    logger.info('load pheno disease molecular-function')
    file_path = os.path.join(CTD_PATH, 'CTD_Phenotype-Disease_molecular_function_associations.tsv.gz')
    names = [
        'GOName',
        'GOID',
        'DiseaseName',
        'DiseaseID',
        'InferenceChemicalQty',
        'InferenceChemicalNames',
        'InferenceGeneQty',
        'InferenceGeneSymbols',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df)


def load_chemical() -> List[dict]:
    logger.info('load chemicals')
    file_path = os.path.join(CTD_PATH, 'CTD_chemicals.tsv.gz')
    names = [
        'ChemicalName',
        'ChemicalID',
        'CasRN',
        'Definition',
        'ParentIDs',
        'TreeNumbers',
        'ParentTreeNumbers',
        'Synonyms',
        'DrugBankIDs',
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df)


def load_disease() -> List[dict]:
    logger.info('load diseases')
    file_path = os.path.join(CTD_PATH, 'CTD_diseases.tsv.gz')
    names = [
        'DiseaseName',
        'DiseaseID',
        'AltDiseaseIDs',
        'Definition',
        'ParentIDs',
        'TreeNumbers',
        'ParentTreeNumbers',
        'Synonyms',
        'SlimMappings'
    ]
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df)


def load_gene() -> List[dict]:
    logger.info('load genes')
    file_path = os.path.join(CTD_PATH, 'CTD_genes.tsv.gz')
    names = ['GeneSymbol', 'GeneName', 'GeneID', 'AltGeneIDs', 'Synonyms', 'BioGRIDIDs', 'PharmGKBIDs', 'UniProtIDs']
    df = pd.read_csv(file_path, sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names)

    return df2records(df)


def load_pathway() -> List[dict]:
    logger.info('load pathways')
    names = ['PathwayName', 'PathwayID']
    df = pd.read_csv(
        os.path.join(CTD_PATH, 'CTD_pathways.tsv.gz'), sep='\t', skiprows=SKIP_ROW_TABLE['bioentity'], names=names
    )

    return df2records(df)


def load_exposure_ontology():
    logger.info('load exposure ontology')
