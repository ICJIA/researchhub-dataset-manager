import pandas as pd
import requests

from io import BytesIO
from zipfile import ZipFile

from util.data.misc import CannotUpdateError, get_year_max

__id = 900

def __filter_illinois(df):
    """Filter to keep bridgepop estimates for Illinois only."""
    pat = f'^\d{{{df["raw_value"].str.len().max() - 17}}}17'
    
    return df \
        .loc[df["raw_value"].str.contains(pat)] \
        .reset_index(drop=True)

def __extract_from_res(res):
    """Extract bridgepop data from http response."""
    try:
        zip = ZipFile(BytesIO(res.content))
        
        return pd.read_table(
                zip.open(zip.namelist()[0]),
                header=None,
                names=['raw_value']
            )
    except:
        raise

def __fetch_from_url(url):
    """Fetch a single-year bridgepop estimates for Illinois."""
    print(f"NOTE: Downloading from '{url}'...")
    res = requests.get(url)

    if res.status_code == 200:
        return res
    elif res.status_code == 404:
        raise CannotUpdateError('ERROR: BridgePop table may be already up to date!')
    else:
        res.raise_for_status()

def __build_url(v, y):
    """Return url for a single-year bridgepop estimates for Illinois.
    
    Args:
        v (int): Version year (YYYY) for bridgepop data.
        y (int): Estimate year (yy) for bridgepop data.
    """
    jul_if_year_zero = '_jul' if y % 10 == 0 else ''
    filename = f'pcen_v{v}_y{y}{jul_if_year_zero}.txt.zip'
    return f'https://www.cdc.gov/nchs/nvss/bridged_race/{filename}'

def __transform_bridgepop(df):
    """Transform bridgepop data into the proper format.
    
    Args:
        df (pandas.DataFrame): BridgePop data in the original format.

    Returns:
        pandas.DataFrame: Transformed data in the proper format.
    """
    try:
        ix = df['raw_value'].str.len().max() - 15
        apply = lambda x, f: x['raw_value'].apply(f)
        fips_to_county_id = lambda s: (int(s[ix:ix+3]) + 1) / 2

        return df \
            .assign(
                year=lambda x: apply(x, lambda s: s[4:8]),
                fk_bridgepop_county=lambda x: apply(x, fips_to_county_id),
                age=lambda x: apply(x, lambda s: s[ix+3:ix+5]),
                race_gender=lambda x: apply(x, lambda s: s[ix+5]),
                hispanic=lambda x: apply(x, lambda s: s[ix+6]),
                value=lambda x: apply(x, lambda s: s[ix+7:])
            ) \
            .drop(['raw_value'], axis=1) \
            .astype(int)
    except:
        raise

def prepare_bridgepop_data(year=None):
    """Prepare the bridgepop data.

    Returns:
        pandas.DataFrame: BridgePop data for Illinois in the original format.
    """
    try:
        v = get_year_max(__id) + 1 if year is None else year
        y = v - 2000
        y_range = range(y - (y % 10), y + 1)

        list_res = [__fetch_from_url(__build_url(v, y)) for y in y_range]

        return pd.concat(
                [__filter_illinois(__extract_from_res(r)) for r in list_res],
                ignore_index=True
            )\
            .pipe(__transform_bridgepop)
    except:
        raise