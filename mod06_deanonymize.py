import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """

    identifiers = ['age', 'gender', 'zip3']
    merged = pd.merge(anon_df, aux_df, on=identifiers, how='inner') 

    match_count_anon = merged.groupby('anon_id')['anon_id'].transform('count') #
    match_count_aux = merged.groupby('name')['name'].transform('count')
    
    unique_matches = merged[(match_count_anon == 1) & (match_count_aux == 1)].copy()
    
    return unique_matches[['anon_id', 'name']].rename(columns={'name': 'matched_name'})
            



def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    return_val = 0
    if(len(anon_df) > 0):
        return_val = len(matches_df) / len(anon_df)
    return return_val
