import pandas as pd
import requests

from io import BytesIO
from zipfile import ZipFile

from util.data.misc import CannotUpdateError, get_year_max

__id = 900

def __filter_illinois(df):
    """Filter to keep bridgepop estimates for Illinois only."""
    pat = f'^\d{{{df["raw_value"].str.len().max() - 17}}}17'
    
    return (
        df[df['raw_value'].str.contains(pat)]
            .reset_index(drop=True)    
    )

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

def __fetch_from_url(v, y):
    """Fetch a single-year bridgepop estimates for Illinois.

    This function fetches a single-year bridgepop estimates data from the source
    ftp server, which contains the Bridged-Race Population Estimates datasets
    prepared by the National Center for Health Statistics of the Centers for
    Disease Control and Prevention.

    Args:
        v (int): Version year (YYYY) for bridgepop data.
        y (int): Estimate year (yy) for bridgepop data.

    Returns:
        pandas.DataFrame: Single year bridgepop estimates for Illinois.
    
    """
    if y % 10 == 0:
        target = f'pcen_v{v}_y{y}_jul.txt.zip'
    else:
        target = f'pcen_v{v}_y{y}.txt.zip'
    
    url = f'https://ftp.cdc.gov/pub/health_statistics/nchs/Datasets/NVSS/bridgepop/{v}/{target}'
    
    res = requests.get(url, verify=False)
    
    if res.status_code == 200:
        return __filter_illinois(__extract_from_res(res))
    elif res.status_code == 404:
        raise CannotUpdateError('ERROR: BridgePop table is already up to date!')
    else:
        res.raise_for_status()

def __transform_bridgepop(df):
    """Transform bridgepop data into the proper format.
    
    Args:
        df (pandas.DataFrame): BridgePop data in the original format.

    Returns:
        pandas.DataFrame: Transformed data in the proper format.
    
    """
    try:
        ix = df['raw_value'].str.len().max() - 15
        fips_to_icjia_num = lambda x: (int(x) + 1)/2

        df['fk_bridgepop_county'] = df['raw_value'] \
            .apply(lambda x: x[ix:ix+3]) \
            .apply(fips_to_icjia_num)
        df['year'] = df['raw_value'].apply(lambda x: x[:4])
        df['age'] = df['raw_value'].apply(lambda x: x[ix+3:ix+5])
        df['race_gender'] = df['raw_value'].apply(lambda x: x[ix+5])
        df['hispanic'] = df['raw_value'].apply(lambda x: x[ix+6])
        df['value'] = df['raw_value'].apply(lambda x: x[ix+7:])
        
        return df.iloc[:, 1:].astype(int)
    except:
        raise

def prepare_bridgepop_data(year=None):
    """Prepare the bridgepop data.

    Returns:
        pandas.DataFrame: BridgePop data for Illinois in the original format.
    """
    try:
        if year is None:
            year = get_year_max(__id) + 1

        v = year + 1
        y = v - 2000
        y_range = range(y - (y % 10), y + 1)

        out = pd.DataFrame()
        for y_i in y_range:
            try:
                out = out.append(__fetch_from_url(v, y_i))
            except:
                raise

        return __transform_bridgepop(out)
    except:
        raise