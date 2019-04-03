import pandas as pd
import re

from util.database.dbread import read_table, read_view
from util.dataset.misc import mask_less_than_10

def __get_dataset_variable(variable, id):
    """Return variables for a specific dataset."""
    try:
        return variable[variable['fk_variable_dataset'] == id]
    except:
        print(f'ERROR: No output is available for dataset ID {id})!')
        raise

def __get_group(dataset, id):
    """Return group value for a specific dataset."""
    try:
        return dataset[dataset['id'] == id].iloc[0, 1]
    except:
        print(f'ERROR: Cannot get group for dataset ID {id}!')
        raise

def __get_dataset_data(data, variable, id):
    """Filter and return Data rows for a specific dataset.

    Args:
        data (pandas.DataFrame): ``Data`` table in database.
        variable (pandas.DataFrame): ``Variable`` table in database.
        id (int): Dataset ID as in the ``Dataset`` table in database.
    
    Returns:
        pandas.DataFrame: Filtered ``Data`` table relevent to a specific data output.

    """
    try:
        var = __get_dataset_variable(variable, id)
        
        filter1 = data['fk_data_variable'].isin(var['id'].tolist())
        filter2 = data['fk_data_county'].isin(list(range(103)))
        return data[filter1 & filter2]
    except:
        print(f'ERROR: Failed to filter Data for dataset id: {id}')
        raise

def __merge_count_county(df, county, variable, id):
    """Merge ``Data`` and ``County`` tables for a specific dataset.

    Args:
        df (pandas.DataFrame): Filtered ``Data`` table for a specific dataset. 
        county (pandas.DataFrame): ``County`` table in database.
        variable (pandas.DataFrame): ``Variable`` table in database.
        id (int): Dataset ID as in the ``Dataset`` table in database.
    
    Returns:
        pandas.DataFrame: Merged table relevent to a specific dataset.

    """
    try:
        var = __get_dataset_variable(variable, id)
        county['percent_rural'] = county['percent_rural'].round(1)
        col_to_drop1 = ['fk_data_variable', 'id'] 
        col_to_drop2 = ['fk_data_county', 'fk_county_typeunit', 'alphabetical_order']
        
        return (
            df
            .merge(
                var[['id', 'name']],
                how='left',
                left_on='fk_data_variable',
                right_on='id'
            )
            .drop(col_to_drop1, axis=1)
            .merge(
                county,
                how='left',
                left_on='fk_data_county',
                right_on='id'
            )
            .drop(col_to_drop2, axis=1)
        )
    except:
        print('ERROR: Cannot merge additional information to filtered Data table!')
        raise

def __pivot_merged(df):
    """Pivot merged table to create a separate column per indicator value.
    
    Args:
        df (pandas.DataFrame): Output of merging filtered ``SimpleCount`` and ``County`` tables for a specific data output.
    
    Returns:
        pandas.DataFrame: Pivoted table where each indicator becomes a column.
    """
    try:
        list_ix = [c for c in df.columns.tolist() if c not in ['name', 'value']]

        df = df.pivot_table(index=list_ix, columns='name', values='value')
        df.columns.name = None

        return df.reset_index()
    except:
        print('ERROR: Cannot pivot to create a separate column per indicator value!')
        raise

def __get_data_with_county(county, data, dataset, variable, id):
    """Return records from ``Data`` table for a specific dataset.

    This function ...

    Args:
        county (pandas.DataFrame): ``County`` table fetched from database.
        data (pandas.DataFrame): ``Data`` table fetched from database.
        dataset (pandas.DataFrame): ``Dataset`` table fetched from database.
        variable (pandas.DataFrame): ``Variable`` table fetched from database.
        id (int): Dataset ID as in the ``Dataset`` table in database.
    
    Returns:
        pandas.DataFrame: Data for a specific dataset.
         
    """
    try:
        df = __get_dataset_data(data, variable, id)
        df = __merge_count_county(df, county, variable, id)
        
        if __get_group(dataset, id) == 2:
            df = mask_less_than_10(df)

        return __pivot_merged(df)
    except:
        print(f'ERROR: Cannot get data for a dataset id: {id}')
        raise

def __get_population_new(type_pop):
    """Return population values since 2000 for a specific population type.

    Args:
        type_pop (int): Code for aggregating population.
    
    Returns:
        pandas.DataFrame: Aggregated population values since 2000 by year and county.
    """
    try:
        bridge_pop = read_table('BridgePop')
        dict_range = {
            '016': range(16+1),
            '017': range(17+1),
            '018': range(18+1),
            '1012': range(10, 12+1),
            '1016': range(10, 16+1),
            '1017': range(10, 17+1),
            '1316': range(13, 16+1),
            '1720': range(17, 20+1),
            '6085': range(60, 85+1),
        }        

        if type_pop == 'all':
            pop = bridge_pop
        elif type_pop in dict_range.keys():
            pop = bridge_pop[bridge_pop['age'].isin(dict_range[type_pop])]
        else:
            raise ValueError("ERROR: Invalid population code!")
        
        return (
            pop
            .groupby(['year', 'fk_bridgepop_county'])
            .value
            .agg('sum')
            .reset_index()
            .sort_values(by='fk_bridgepop_county', kind='mergesort')
            .sort_values(by='year', ascending=False, kind='mergesort')
        )
    except:
        print("ERROR: Cannot aggregate population!")
        raise

def __get_population_old(type_pop):
    """Return population values before 2000 for a specific population type.
    
    Args:
        type_pop (int): Population type for age group.
    
    Returns:
        pandas.DataFrame: Aggregated population values before 2000 by year and county.
    """
    try:
        bridge_pop_old = read_table('BridgePopOld')

        return (
            bridge_pop_old[
                (bridge_pop_old['fk_bridgepop_typepop'] == type_pop) &
                (bridge_pop_old['year'] < 2000) &
                (bridge_pop_old['fk_bridgepop_county'] < 103)]
            .drop('fk_bridgepop_typepop', axis=1)
            .sort_values(by='fk_bridgepop_county', kind='mergesort')
            .sort_values(by='year', ascending=False, kind='mergesort')
        )
    except:
        print(f"ERROR: Cannot get population for population code: {type_pop}!")
        raise

def __get_population(type_pop):
    """Return population values for a specific population type.

    Args:
        type_pop (int): Population type for age group.
    
    Returns:
        pandas.DataFrame: Aggregated population values by year and county.
    """
    try:
        pop_new = __get_population_new(type_pop)
        pop_old = __get_population_old(type_pop)
        
        pop = pop_new.append(pop_old, sort=True)
        pop.columns = ['id', 'population', 'year']
        
        return pop.reset_index(drop=True)
    except:
        print(f"ERROR: Cannot get population for population code: {type_pop}!")
        raise

def __get_population_adult():
    """Return mixted adult population values."""
    try:
        pop_016 = __get_population('016')
        pop_017 = __get_population('017')
        pop_all = __get_population('all')

        pop_y_before = pop_016[pop_016['year'] <= 2010]
        pop_y_after = pop_017[pop_017['year'] > 2010]

        pop_young = pop_y_before.append(pop_y_after, sort=True).reset_index(drop=True)
        pop_adult = pop_young.merge(pop_all, how='left', on=['id', 'year'])
        pop_adult['population'] = pop_adult['population_y'] - pop_adult['population_x']

        return pop_adult[['id', 'population', 'year']]
    except:
        print("ERROR: Cannot get adult population!")
        raise

def __get_population_juvenile():
    """Return mixed juvenile population values."""
    try:
        pop_1016 = __get_population('1016')
        pop_1017 = __get_population('1017')
        
        pop_before = pop_1016[pop_1016['year'] <= 2010]
        pop_after = pop_1017[pop_1017['year'] > 2010]

        return pop_before.append(pop_after, sort=True).reset_index(drop=True)
    except:
        print("ERROR: Cannot get juvenile population!")
        raise

def __generate_standard_data(dataset, id):
    """Return a processed table for a standard data output.

    Args:
        id (int): Dataset ID as in the ``Dataset`` table in database.

    Returns:
        pandas.DataFrame: A specified standard dataset table with counts and rates.
    """
    try:
        county = read_table('County')
        data = read_table('Data')
        variable = read_table('Variable')

        var = __get_dataset_variable(variable, id)
        type_rate = var['fk_variable_typerate'].iloc[0,]
        type_pop = var['fk_variable_typepop'].iloc[0,]
        unit_rate = { 0: None, 1: 100000,  2: 100 }.get(type_rate, 1)

        if type_pop == 'juv':
            pop = __get_population_juvenile()
        elif type_pop == 'adt':
            pop = __get_population_adult()
        else:
            pop = __get_population(type_pop)

        df = __get_data_with_county(county, data, dataset, variable, id)
        df = df.merge(pop, how='left', on=['year', 'id'])
        list_col = df.columns.tolist()
        df = df[list_col[:8] + [list_col[-1]] + list_col[8:-1]]

        if unit_rate:
            list_val = df.columns.tolist()[9:]
            for val in list_val:
                val_rate = round(df[val] / df['population'] * unit_rate, 1)
                df[f'{val}_rate'] = val_rate
        
        return df
    except:
        print(f"ERROR: Cannot generate standard type data for dataset ID {dataset}!")
        raise

def __generate_nonstandard_data(dataset, id):
    """Return a processed table for a non-standard data output.

    Args:
        id (int): Output ID as in the ``Output`` table in database.

    Returns:
        pandas.DataFrame: A specified non-standard output table.
    """
    try:
        name = dataset[dataset['id'] == id]['name'].iloc[0]
        
        if name == 'employment':
            county = read_table('County')
            data = read_table('Data')
            variable = read_table('Variable')
            
            df = __get_data_with_county(county, data, dataset, variable, id)
            df['unemployment_rate'] = df['unemployed'] / df['labor_force_population'] * 100
            df['unemployment_rate'] = df['unemployment_rate'].round(1)
            list_col = df.columns.tolist()
            
            return df[list_col[:8] + ['labor_force_population', 'employed'] + list_col[10:]]
        elif name == 'illinois_population':
            return read_view('vIllinoisPopulation')
        elif name == 'illinois_population_old':
            return read_view('vIllinoisPopulationOld')
    except:
        print(f"ERROR: Cannot generate non-standard type data for dataset ID {dataset}!")
        raise

def generate_data(id):
    """Return a processed table for a specific data output.

    This funtion uses values in ``SimpleCount`` or ``Population`` in
    the database (``@/database/cjia_webdata.db``) to generate a data output of
    choice as specified by the ``id`` input.

    Args:
        id (int): Output ID as in the ``Output`` table in database.

    Returns:
        pandas.DataFrame: A specified output table.

    """
    try:
        dataset = read_table('Dataset')
        title = dataset[dataset['id'] == id]['name'].tolist()[0]

        active = dataset[dataset['id'] == id]['active'].tolist()[0] == 1
        standard = dataset[dataset['id'] == id]['standard'].tolist()[0] == 1
        
        if active:
            if standard:
                return __generate_standard_data(dataset, id)
            else:
                return __generate_nonstandard_data(dataset, id)
        else:
            raise ValueError(f"ERROR: {title} currently not active!")
    except:
        raise