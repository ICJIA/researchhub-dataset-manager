"""Offer functions for generating outputs in the drive.

This module offer functions to generate outputs in the drive.
The module depends on the ``database`` module.

The module contains the following public functions to be called externally:

``init()`` initializes the ``outputtools`` module.
``create_temp()`` creates a temporary table in ``@/temp``.
``delete_temp()`` deletes temporary tables in ``@/temp``.
``generate_package()`` generates a packaged dataset in ``@/dataset``.
``generate_packages_by_source_group()` generates dataset packages for a provided source group.
"""
import math
import os
import re
import zipfile

from . import database

def init():
    """Initialize the ``outputtools`` module.

    The function checks whether the database connection is established
    and calls ``database.init()`` if not.
    
    """
    try:
        database.CONN
    except (AttributeError, NameError):
        database.init()
    
    global _CONN

    _CONN = database.CONN

# functions to handle temporary outputs
def _create_file(df, dirname, filename):
    """Create comma-separated values file from a pandas DataFrame.

    Args:
        df (pandas DataFrame): Data input.
        dirname (str): Directory name to save a output file.
        filename (str): Output file name.

    """
    path = f'P:\\DATA\\CJIA_WebData\\{dirname}\\{filename}.csv'
    df.to_csv(path, index=False)

def _delete_file(dirname, filename):
    """Delete comma-separated values file.

    Args:
        df (pandas DataFrame): Data input.
        dirname (str): Directory name to save a output file.
        filename (str): Output file name.
    
    """
    path = f'P:\\DATA\\CJIA_WebData\\{dirname}\\{filename}.csv'
    if os.path.isfile(path):
        os.remove(path)
    else:
        print(f'"{filename}.csv" file not found in "{dirname}" directory.')

def _list_files(dirname):
    """Return a list of filenames in a directory."""
    path = f'P:\\DATA\\CJIA_WebData\\{dirname}'
    return os.listdir(path)

def create_temp(df, name_temp):
    """Create a temporary table in ``@/temp``.

    This function creates a temporary table with the given name and saves it in
    ``@/temp``.
    
    Args:
        df (pandas DataFrame): Data for the temporary table.
        name_temp (str): Name of the temporary table.
    
    Returns:
        bool: True for success, False otherwise.

    """
    try:
        if database.validate_temp_table_name(name_temp):
            _create_file(df, 'temp', name_temp)
            print(f'NOTE: "{name_temp}" is successfully generated in /temp/.')
    except:
        print(f'ERROR: Cannot generate "{name_temp}".')
        raise

def delete_temp(name_temp=None):
    """Delete temporary tables in ``@/temp``.

    This function deletes temporary tables in ``@/temp``. If ``name`` is given,
    only a table with the given name will be deleted. Otherwise, all tables with
    "Temp" in their names will be deleted. 

    Args:
        name_temp (str): Name of a temporary table to delete. Default is None. If None, all temporary tables will be deleted.
    
    Returns:
        bool: True for success, False otherwise.

    """
    try:
        if name_temp == None:
            filenames = _list_files('temp')
            for filename in filenames:
                filename = re.sub('\..*', '', filename)
                if database.validate_temp_table_name(filename):
                    _delete_file('temp', filename)
                    print(f'NOTE: "{filename}" is successfully removed from /temp/.')
        else:
            if database.validate_temp_table_name(name_temp):
                _delete_file('temp', name_temp)
                print(f'NOTE: "{name_temp}" is successfully removed from /temp/.')
    except:
        raise

# functions to generate dataset outputs
def _get_indicator_for_output(indicator, out_id):
    """Return indicators for a specific data output.

    Args:
        indicator (pandas.DataFrame): ``Indicator`` table fetched from database.
        out_id (int): Output ID as in the ``Output`` table in database.
    
    Returns:
        pandas.DataFrame: Rows from ``Indicator`` table relevent to a specific data output.
    """
    try:
        return indicator[indicator['fk_indicator_output'] == out_id]
    except:
        print(f'ERROR: No output is available for the provided input (output id {out_id}).')
        raise

def _get_output_source_group(output, out_id):
    """Return output source group number for a specific data output."""
    try:
        return output[output['id'] == out_id].iloc[0, 1]
    except:
        print(f'ERROR: Cannot get output source group for output id {out_id}!')
        raise

def _filter_simplecount(simplecount, indicator, out_id):
    """Filter and return SimpleCount rows for a specific data output.

    Args:
        simplecount (pandas.DataFrame): ``SimpeleCount`` table fetched from database.
        indicator (pandas.DataFrame): ``Indicator`` table fetched from database.
        out_id (int): Output ID as in the ``Output`` table in database.
    
    Returns:
        pandas.DataFrame: Filtered ``SimpleCount`` table relevent to a specific data output.

    """
    try:
        ind = _get_indicator_for_output(indicator, out_id)

        filter1 = simplecount['fk_simplecount_indicator'].isin(ind['id'].tolist())
        filter2 = simplecount['fk_simplecount_county'].isin(list(range(103)))
        return simplecount[filter1 & filter2]
    except:
        print(f'ERROR: Failed to filter simplecount for data output id: {out_id}')
        raise

def _merge_to_filtered(filtered, county, indicator, out_id):
    """Merge ``County`` and ``SimpleCount`` tables for a specific data output.

    Args:
        filtered (pandas.DataFrame): Filtered ``SimpeleCount`` table for a specific data output. 
        county (pandas.DataFrame): ``County`` table fetched from database.
        indicator (pandas.DataFrame): ``Indicator`` table fetched from database.
        out_id (int): Output ID as in the ``Output`` table in database.
    
    Returns:
        pandas.DataFrame: Merged table relevent to a specific data output.

    """
    try:
        ind = _get_indicator_for_output(indicator, out_id)
        county['percent_rural'] = county['percent_rural'].round(1)
        col_to_drop1 = ['fk_simplecount_indicator', 'id'] 
        col_to_drop2 = [
                'fk_simplecount_county',
                'judicial_circuit',
                'fk_county_geography',
                'alphabetical_order'
            ]
        
        return (
            filtered
            .merge(
                ind[['id', 'name']],
                how='left',
                left_on='fk_simplecount_indicator',
                right_on='id')
            .drop(col_to_drop1, axis=1)
            .merge(
                county,
                how='left',
                left_on='fk_simplecount_county',
                right_on='id'
            )
            .drop(col_to_drop2, axis=1)
        )
    except:
        print('ERROR: Cannot merge additional information to filtered count table!')
        raise

def _mask_less_than_10(df):
    """Mask count values less than 10 to minimize identifiability.
    
    Args:
        df (pandas.DataFrame): (Transformed) ``SimpleCount`` table.

    Returns:
        pandas.DataFrame: Masked table where values less than 10 are removed.
    """
    try:
        masked = df.copy()
        masked.ix[masked.value < 10, 'value'] = math.nan
        return masked
    except:
        print('ERROR: Cannot mask values less than 10!')
        raise

def _pivot_merged(merged):
    """Pivot merged table to create a separate column per indicator value.
    
    Args:
        merged (pandas.DataFrame): Output of merging filtered ``SimpleCount`` and ``County`` tables for a specific data output.
    
    Returns:
        pandas.DataFrame: Pivoted table where each indicator becomes a column.
    """
    try:
        index_list = [c for c in merged.columns.tolist() if c not in ['name', 'value']]

        out = merged.pivot_table(index=index_list, columns='name', values='value')
        out.columns.name = None

        return out.reset_index()
    except:
        print('ERROR: Cannot pivot to create a separate column per indicator value!')
        raise

def _get_count(simplecount, county, output, indicator, out_id):
    """Return count data from ``SimpleCount`` table for a specific data output.

    This function ...

    Args:
        simplecount (pandas.DataFrame): ``SimpeleCount`` table fetched from database.
        county (pandas.DataFrame): ``County`` table fetched from database.
        output (pandas.DataFrame): ``Output`` table fetched from database.
        indicator (pandas.DataFrame): ``Indicator`` table fetched from database.
        out_id (int): Output ID as in the ``Output`` table in database.
    
    Returns:
        pandas.DataFrame: Count table for a specific data output.
         
    """
    try:
        filtered = _filter_simplecount(simplecount, indicator, out_id)
        merged = _merge_to_filtered(filtered, county, indicator, out_id)
        
        if _get_output_source_group(output, out_id) == 2:
            return _pivot_merged(_mask_less_than_10(merged))
        else:
            return _pivot_merged(merged)
    except:
        print(f'ERROR: Cannot get count table for a data output id: {out_id}')
        raise

def _aggregate_population(population, population_code):
    """Aggregate population values in the ``Population`` table for a specific population code.

    Args:
        population (pandas.DataFrame): ``Population`` table fetched from database.
        population_code (int): Code for aggregating population.
    
    Returns:
        pandas.DataFrame: Table of aggregated population values by year and county.
    """
    try:
        if population_code == 1000:
            pop = population
        elif population_code == 1001:
            pop = population[population['age'].isin(range(60, 85+1))]
        elif population_code == 1002:
            pop = population[population['age'].isin(range(16+1))]
        elif population_code == 1003:
            pop = population[population['age'].isin(range(17+1))]
        elif population_code == 1004:
            pop = population[population['age'].isin(range(10, 16+1))]
        elif population_code == 1005:
            pop = population[population['age'].isin(range(13, 16+1))]
        elif population_code == 1006:
            pop = population[population['age'].isin(range(18+1))]
        elif population_code == 1007:
            pop = population[population['age'].isin(range(10, 12+1))]
        elif population_code == 1008:
            pop = population[population['age'].isin(range(10, 17+1))]
        elif population_code == 1009:
            pop = population[population['age'].isin(range(17, 20+1))]    
        else:
            raise ValueError('ERROR: Invalid population code!')
        
        return (
            pop
            .groupby(['year', 'fk_population_county'])
            .value
            .agg('sum')
            .reset_index()
            .sort_values(by='fk_population_county', kind='mergesort')
            .sort_values(by='year', ascending=False, kind='mergesort')
        )
    except:
        print('ERROR: Cannot aggregate population!')
        raise

def _get_population(population, population_old, population_code):
    """Return population values using the ``Population`` and ``PopulationOld`` tables for a specific population code.

    Args:
        population (pandas.DataFrame): ``Population`` table fetched from database.
        population_old (pandas.DataFrame): ``PopulationOld`` table fetched from database.
        population_code (int): Code for aggregating population.
    
    Returns:
        pandas.DataFrame: Table of aggregated population values by year and county.
    """
    try:
        pop_new = _aggregate_population(population, population_code)
        pop_old = population_old[
                (population_old['fk_population_indicator'] == population_code) &
                (population_old['year'] < 2000) &
                (population_old['fk_population_county'] < 103)] \
            .drop('fk_population_indicator', axis=1) \
            .sort_values(by='fk_population_county', kind='mergesort') \
            .sort_values(by='year', ascending=False, kind='mergesort')
        
        pop = pop_new.append(pop_old)
        pop.columns = ['id', 'population', 'year']
        
        return pop.reset_index(drop=True)
    except:
        print(f'ERROR: Cannot get population for population code: {population_code}')
        raise

def _get_juv_population(population, population_old):
    """Return mixed juvenile population values using the ``Population`` and ``PopulationOld`` tables.

    Args:
        population (pandas.DataFrame): ``Population`` table fetched from database.
        population_old (pandas.DataFrame): ``PopulationOld`` table fetched from database.
    
    Returns:
        pandas.DataFrame: Table of aggregated population values by year and county.
    """
    try:
        pop_1016 = _get_population(population, population_old, 1004)
        pop_1017 = _get_population(population, population_old, 1008)
        
        pop_before = pop_1016[pop_1016['year'] <= 2010]
        pop_after = pop_1017[pop_1017['year'] > 2010]

        return pop_before.append(pop_after).reset_index(drop=True)
    except:
        print('ERROR: Cannot get juvenile population!')
        raise

def _generate_standard_output(out_id):
    """Return a processed table for a standard data output.

    Args:
        out_id (int): Output ID as in the ``Output`` table in database.

    Returns:
        pandas.DataFrame: A specified standard output table with counts and rates.
    """
    try:
        name_list = [
            'County',
            'Indicator',
            'Population',
            'PopulationOld',
            'SimpleCount',
            'Output'
        ]
        county, indicator, population, population_old, simplecount, output = database.fetch_tables(name_list)

        ind = _get_indicator_for_output(indicator, out_id)       
        count = _get_count(simplecount, county, output, indicator, out_id)
        rate_type = ind['fk_indicator_ratedivisor'].iloc[0,]
        pop_code = ind['fk_indicator_population_indicator'].iloc[0,]
        multiplier = 1

        if pop_code == 1040:
            pop = _get_juv_population(population, population_old)
        else:
            pop = _get_population(population, population_old, pop_code)

        if rate_type == 1:
            multiplier = 100000
        elif rate_type == 2:
            multiplier = 100

        out = count.merge(pop, how='left', on=['year', 'id'])
        col_list = out.columns.tolist()
        out = out[col_list[:7] + [col_list[-1]] + col_list[7:-1]]
        
        val_list = out.columns.tolist()[8:]
        for val in val_list:
            out[f'{val}_rate'] = round(out[val] / out['population'] * multiplier, 1)

        return out
    except:
        raise

def _generate_nonstandard_output(out_id):
    """Return a processed table for a non-standard data output.

    Args:
        out_id (int): Output ID as in the ``Output`` table in database.

    Returns:
        pandas.DataFrame: A specified non-standard output table.
    """
    try:
        name_list = [
            'County',
            'Indicator',
            'Population',
            'PopulationOld',
            'SimpleCount',
            'Output'
        ]
        county, indicator, population, population_old, simplecount, output = database.fetch_tables(name_list)

        name = output[output['id'] == out_id]['name'].iloc[0]

        if name == 'employment':
            out = _get_count(simplecount, county, output, indicator, out_id)
            out['unemployment_rate'] = out['unemployed'] / out['labor_force_population'] * 100
            out['unemployment_rate'] = out['unemployment_rate'].round(1)
            column_list = out.columns.tolist()

            return out[column_list[:7] + ['labor_force_population', 'employed'] + column_list[9:]]
        elif name in ['illinois_population', 'illinois_population_old']:
            if name == 'illinois_population':
                pop = population.copy()
                pop.columns = ['year', 'id', 'age','race_gender', 'hispanic', 'value']
            elif name == 'illinois_population_old':
                pop = population_old.copy()
                pop.columns = ['id', 'year', 'population_code', 'value']
                               
            county['percent_rural'] = county['percent_rural'].round(1)
            column_to_keep = ['year', 'id', 'fips_number', 'county_name'] +\
                ['region', 'commuity_type', 'percent_rural'] +\
                pop.columns.tolist()[2:]

            return pop.merge(county, how='left')[column_to_keep]
        elif name == 'school_enrollment':
            pass
    except:
        raise

def _generate_output(out_id):
    """Return a processed table for a specific data output.

    This funtion uses values in ``SimpleCount`` or ``Population`` in
    the database (``@/database/cjia_webdata.db``) to generate a data output of
    choice as specified by the ``out_id`` input.

    Args:
        out_id (int): Output ID as in the ``Output`` table in database.

    Returns:
        pandas.DataFrame: A specified output table.

    """
    try:
        output = database.fetch_tables(['Output'])[0]
        name = output[output['id'] == out_id]['name'].tolist()[0]

        active = output[output['id'] == out_id]['active'].tolist()[0] == 1
        standard = output[output['id'] == out_id]['standard'].tolist()[0] == 1
        
        if active:
            if standard:
                return _generate_standard_output(out_id)
            else:
                return _generate_nonstandard_output(out_id)
        else:
            raise ValueError(f'ERROR: The specificed output with id {out_id} is currently not active.')
    except:
        raise

def _generate_outputs(pkg_id):
    """Generate multiple processed data output tables.

    This function takes a list of names and generates all datasets specified by
    the given names.

    Args:
        pkg_id (int): A package id for datasets to generate.
    
    Return:
        list: A list of dataset outputs as pandas.DataFrame. 

    """
    try:
        output = database.fetch_table('Output')
        out_id_list = output[output['fk_output_package'] == pkg_id]['id'].unique().tolist()
        
        out_list = []
        for out_id in out_id_list:
            out_list.append(_generate_output(out_id))
        
        return out_list
    except:
        raise

def _create_readme(pkg_id):
    """Return a string of REAMDE text for the specified dataset package."""
    try:
        output = database.fetch_tables(['Output'])[0]
        out_pkg = output[output['fk_output_package'] == pkg_id] \
            .drop(columns=['old_name']) \
            .drop_duplicates() \
            .reset_index(drop=True)
        max_year = int(out_pkg['year_max'].max())

        readme_pkg = 'This zip file contains a number of materials related ' +\
            'to the dataset you downloaded. These include:\r\n\r\n'
        readme_pkg += '* README.txt: This file.\r\n'
        
        readme_list = []
        for i in range(out_pkg.shape[0]):
            readme_pkg += f'* {max_year}_{out_pkg["name"][i]}.csv: ' +\
                f'{out_pkg["name_full"][i]} data in the comman-separated value format\r\n'
            readme_pkg += f'* metadata_{max_year}_{out_pkg["name"][i]}.txt: ' +\
                f'Detailed information about {max_year}_{out_pkg["name"][i]}.csv\r\n'
            
            readme_tbl = f'{out_pkg["name_full"][i]}\r\n'
            readme_tbl += f'{out_pkg["year_type"][i]} Year Range: ' +\
                f'{int(out_pkg["year_min"][i])}-{int(out_pkg["year_max"][i])}\r\n'
            readme_tbl += f'Source: {out_pkg["source"][i]}\r\n\r\n'
            
            readme_tbl += f'DESCRIPTION\r\n{out_pkg["description"][i]}\r\n\r\n'
            
            readme_tbl += f'NOTES\r\n'
            notes = out_pkg['notes'][i]
            notes = notes.split('|') if notes is not None else ['(N/A)']
            for note in notes:
                readme_tbl += f'* {note}\r\n'
            
            readme_tbl += '\r\nCOLUMNS\r\n'
            column_name = out_pkg['column_name'][i].split('|')
            column_info = out_pkg['column_info'][i].split('|')
            for k in range(len(column_name)):
                readme_tbl += f'* {column_name[k]}: {column_info[k]}\r\n'

            readme_list.append(readme_tbl)
 
        readme_pkg += '\r\nThis dataset is prepared and published by ' +\
            'Illinois Criminal Justice Information Authority (ICJIA). ' +\
            'Visit http://icjia.state.il.us to learn more about ICJIA.'
        readme_list.insert(0, readme_pkg)
        
        return readme_list
    except:
        raise

def generate_package(pkg_id):
    """Generate a packaged dataset in ``@/dataset``.

    This function generates a zipped file of a packaged dataset,
    consisting of data outputs in the comma-separated value (CSV) format
    as well as a README text file. Each generated package will be stored
    in ``@/dataset``. If a dataset of the same name already exists,
    the function will overwrite it.
    
    Args:
        package_name (str): Name of a packaged dataset to generate.
        out_list (list): List of pandas.DataFrame objects for data files. 
        name_list (list): List of str for names of data files.

    """

    try:
        output, package = database.fetch_tables(['Output', 'Package'])
        out_list = _generate_outputs(pkg_id)
        
        package_name = package[package['id'] == pkg_id]['name'].tolist()[0]
        name_list = output[output['fk_output_package'] == pkg_id]['name'].unique().tolist()
        readme_list = _create_readme(pkg_id)
        max_year = int(output[output['fk_output_package'] == pkg_id]['year_max'].max())
        
        path = f'P:\\DATA\\CJIA_WebData\\datasets\\{package_name}.zip'
        with zipfile.ZipFile(path, 'w') as z:
            for i in range(len(out_list)):
                z.writestr(f'{max_year}_{name_list[i]}.csv', out_list[i].to_csv(index=False))
                z.writestr(f'metadata_{max_year}_{name_list[i]}.txt', readme_list[i+1])
            z.writestr('README.txt', readme_list[0])
        
        print(f'NOTE: Dataset "{package_name}" is successfully generated!')
        return True
    except Exception as e:
        print(e)
        return False

def generate_packages_by_source_group(source_group):
    """Generate dataset packages for a provided source group."""
    try:
        output = database.fetch_table('Output')
        out_source = output[output['source_group'] == source_group]
        pkg_id_list = out_source['fk_output_package'].unique().tolist()
        for pkg_id in pkg_id_list:
            generate_package(pkg_id)
        
        return True
    except Exception as e:
        print(e)
        return False