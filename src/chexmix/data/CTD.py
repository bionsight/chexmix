import logging
import os

import pandas as pd

from chexmix.env import data_path

logger = logging.getLogger(__name__)
CTD_PATH = os.path.join(data_path, 'ctd')


def df2records(df, float_col=[]):
    records = df.to_dict('records')
    return [{k: (v if (not isinstance(v, float) or (k in float_col)) else int(v))
             for k, v in row.items() if not pd.isnull(v)}
            for row in records]


def load_chemical_gene_interaction():
    logger.info('load chemical gene interaction')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_chem_gene_ixns.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['ChemicalName', 'ChemicalID', 'CasRN', 'GeneSymbol', 'GeneID',
                            'GeneForms', 'Organism', 'OrganismID', 'Interaction',
                            'InteractionActions', 'PubMedIDs'])

    return df2records(df)


def load_chemical_gene_interaction_types():
    logger.info('load chemical gene interaction types')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_chem_gene_ixn_types.tsv'),
                     sep='\t',
                     skiprows=26,
                     names=['TypeName', 'Code',	'Description', 'ParentCode'])

    return df2records(df)


def load_chemical_disease_associations():
    logger.info('load chemical disease associations')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_chemicals_diseases.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['ChemicalName', 'ChemicalID', 'CasRN', 'DiseaseName', 'DiseaseID',
                            'DirectEvidence', 'InferenceGeneSymbol', 'InferenceScore', 'OmimIDs',
                            'PubMedIDs'])

    return df2records(df, ['InferenceScore'])


def load_chemical_go_associations():
    logger.info('load chemical go associations')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_chem_go_enriched.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['ChemicalName', 'ChemicalID', 'CasRN', 'Ontology', 'GOTermName',
                            'GOTermID', 'HighestGOLevel', 'PValue', 'CorrectedPValue', 'TargetMatchQty',
                            'TargetTotalQty', 'BackgroundMatchQty', 'BackgroundTotalQty'])

    return df2records(df, ['PValue', 'CorrectedPValue'])


def load_chemical_pathway_associations():
    logger.info('load chemical pathway associations')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_chem_pathways_enriched.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['ChemicalName', 'ChemicalID', 'CasRN', 'PathwayName', 'PathwayID',
                            'PValue', 'CorrectedPValue', 'TargetMatchQty', 'TargetTotalQty', 'BackgroundMatchQty',
                            'BackgroundTotalQty'])
    return df2records(df, ['PValue', 'CorrectedPValue'])


def load_gene_disease_associations():
    logger.info('load gene disease associations')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_genes_diseases.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['GeneSymbol', 'GeneID', 'DiseaseName', 'DiseaseID',	'DirectEvidence',
                            'InferenceChemicalName', 'InferenceScore', 'OmimIDs', 'PubMedID'])

    return df2records(df, ['InferenceScore'])


def load_gene_pathway_associations():
    logger.info('load gene pathway associations')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_genes_pathways.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['GeneSymbol', 'GeneID', 'PathwayName', 'PathwayID'])
    return df2records(df)


def load_disease_pathway_associations():
    logger.info('load disease pathway associations')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_diseases_pathways.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['DiseaseName', 'DiseaseID', 'PathwayName', 'PathwayID', 'InferenceGeneSymbol'])

    return df2records(df)


def load_chem_pheno_interactions():
    logger.info('load chem phenotype interactions')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_pheno_term_ixns.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['ChemicalName', 'ChemicalID', 'CasRN', 'PhenotypeName', 'PhenotypeID',
                            'ComentionedTerms', 'Organism', 'OrganismID', 'Interaction', 'InteractionActions',
                            'AnatomyTerms', 'InferenceGeneSymbols', 'PubMedIDs'])

    return df2records(df)


def load_exposure_study_associations():
    logger.info('load exposure study interactions')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_exposure_studies.tsv.gz'),
                     sep='\t',
                     skiprows=28,
                     names=['Reference', 'StudyFactors', 'ExposureStressors', 'Receptors', 'StudyCountries',
                            'Mediums', 'ExposureMarkers', 'Diseases', 'Phenotypes', 'AuthorSummary'])

    return df2records(df)


def load_exposure_event_associations():
    logger.info('load exposure event interactions')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_exposure_events.tsv.gz'),
                     sep='\t',
                     skiprows=28,
                     names=['ExposureStressorName', 'ExposureStressorID', 'StressorSourceCategory',
                            'StressorSourceDetails', 'NumberOfStressorSamples', 'StressorNotes',
                            'NumberOfReceptors', 'Receptors', 'ReceptorNotes', 'SmokingStatus', 'Age',
                            'AgeUnitsOfMeasurement', 'AgeQualifier', 'Sex', 'Race', 'Methods', 'DetectionLimit',
                            'DetectionLimitUOM', 'DetectionFrequency', 'Medium', 'ExposureMarker', 'ExposureMarkerID',
                            'MarkerLevel', 'MarkerUnitsOfMeasurement',	'MarkerMeasurementStatistic', 'AssayNotes',
                            'StudyCountries', 'StateOrProvince', 'CityTownRegionArea', 'ExposureEventNotes',
                            'OutcomeRelationship', 'DiseaseName', 'DiseaseID', 'PhenotypeName', 'PhenotypeID',
                            'PhenotypeActionDegreeTypeAnatomy', 'ExposureOutcomeNotes', 'Reference',
                            'AssociatedStudyTitles', 'EnrollmentStartYear', 'EnrollmentEndYear', 'StudyFactors'])

    return df2records(df)


def load_pheno_disease_bioprocess_associations():
    logger.info('load pheno disease bio-process')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_Phenotype-Disease_biological_process_associations.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['GOName', 'GOID', 'DiseaseName', 'DiseaseID', 'InferenceChemicalQty',
                            'InferenceChemicalNames', 'InferenceGeneQty', 'InferenceGeneSymbols'])

    return df2records(df)


def load_pheno_disease_cellcomp_associations():
    logger.info('load pheno disease cellular-component')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_Phenotype-Disease_cellular_component_associations.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['GOName', 'GOID', 'DiseaseName', 'DiseaseID', 'InferenceChemicalQty',
                            'InferenceChemicalNames', 'InferenceGeneQty', 'InferenceGeneSymbols'])

    return df2records(df)


def load_pheno_disease_mole_fn_associations():
    logger.info('load pheno disease molecular-function')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_Phenotype-Disease_molecular_function_associations.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['GOName', 'GOID', 'DiseaseName', 'DiseaseID', 'InferenceChemicalQty',
                            'InferenceChemicalNames', 'InferenceGeneQty', 'InferenceGeneSymbols'])

    return df2records(df)


def load_chemical():
    logger.info('load chemicals')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_chemicals.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['ChemicalName', 'ChemicalID', 'CasRN', 'Definition', 'ParentIDs', 'TreeNumbers',
                            'ParentTreeNumbers', 'Synonyms', 'DrugBankIDs'])

    return df2records(df)


def load_disease():
    logger.info('load diseases')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_diseases.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['DiseaseName', 'DiseaseID', 'AltDiseaseIDs', 'Definition', 'ParentIDs', 'TreeNumbers',
                            'ParentTreeNumbers', 'Synonyms', 'SlimMappings'])

    return df2records(df)


def load_gene():
    logger.info('load genes')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_genes.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['GeneSymbol', 'GeneName', 'GeneID', 'AltGeneIDs', 'Synonyms', 'BioGRIDIDs',
                            'PharmGKBIDs', 'UniProtIDs'])

    return df2records(df)


def load_pathway():
    logger.info('load pathways')
    df = pd.read_csv(os.path.join(CTD_PATH, 'CTD_pathways.tsv.gz'),
                     sep='\t',
                     skiprows=29,
                     names=['PathwayName', 'PathwayID'])

    return df2records(df)


def load_exposure_ontology():
    logger.info('load exposure ontology')
