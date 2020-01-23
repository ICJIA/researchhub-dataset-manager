from math import nan

def mask_less_than_10(df):
    """Mask raw values less than 10 to minimize identifiability.
    
    Args:
        df (pandas.DataFrame): Transformed ``Data`` table.

    Returns:
        pandas.DataFrame: Masked table where values less than 10 are removed.
    """
    try:
        df.ix[df.value < 10, 'value'] = nan
        return df
    except:
        print("ERROR: Cannot mask values less than 10!")
        raise