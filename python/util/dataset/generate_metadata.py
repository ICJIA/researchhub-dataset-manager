from util.database.dbread import read_table

def __generate_sources(info):
    """Return a list of metadata dictionaries for sources."""
    
    source = { 'title': info['source'].iloc[0] }
    if info['source_url'] is not None:
        source['url'] = info['source_url'].iloc[0]

    return [source]

def __generate_time_period(info):
    """Return a metadata dictionary for time period."""
    return {
        'yeartype': info['year_type'].iloc[0],
        'yearmin': int(info['year_min'].iloc[0]),
        'yearmax': int(info['year_max'].iloc[0])
    }

def __generate_metadata_variables_common(standard):
    """Return a list of metadata dictionaries for common variables."""
    metadata = [
        {
            'name': 'year',
            'type': 'int',
            'definition': 'Data year.'
        },
        {
            'name': 'id',
            'type': 'int',
            'definition': 'Location identifier.'
        },
        {
            'name': 'fips',
            'type': 'int',
            'definition': 'Federal Information Processing Standard (FIPS) code.'
        },
        {
            'name': 'county',
            'type': 'str',
            'definition': 'County name.'
        },
        {
            'name': 'region',
            'type': 'str',
            'definition': 'Region of a county',
            'values': 'Northen minus Cook, Northenr - Cook, Central, or Southern.'
        },
        {
            'name': 'community_type',
            'type': 'str',
            'definition': 'Categorization based on the proportion of rural area in a county.',
            'values': 'Completely Rural (rural 100%), Mostly rural (rural >50%), Mostly urban (rural <50%), or Completely urban (rural 0%).'
        },
        {
            'name': 'percent_rural',
            'type': 'float',
            'definition': 'Percentage of rural area in a county.',
            'values': '0.0 to 100.0.'
        }
    ]
    
    if standard:
        metadata.append({
            'name': 'percent_rural',
            'type': 'int',
            'definition': 'Population estimate.',
            'values': 'Non-negative.'
        })
    
    return metadata

def __generate_metadata_variable_count(var):
    """Generate a metadata dictionary for each count variable."""
    name = var['name'].iloc[0]
    definition = var['definition'].iloc[0]

    return {
        'name': f"{name}_rate",
        'type': 'int',
        'definition': definition,
        'values': 'Non-negative.'
    }

def __generate_metadata_variable_rate(var):
    """Generate a metadata dictionary for each rate variable."""
    typerate = var['fk_variable_typerate'].iloc[0]
    dict_rate = {
        1: 'per 100,000',
        2: 'per cent'
    }

    if typerate in dict_rate.keys():
        percent = typerate == 2
        name = var['name'].iloc[0]
        return {
            'name': f"{name}_rate",
            'type': 'float',
            'definition': f"Rate for {name}, {dict_rate[typerate]}.\n",
            'values': '0.0 to 100.0.' if percent else 'Non-negative.'
        }

def __generate_metadata_variables(id, standard):
    """Generate a list of metadata dictionaries for variables."""
    try:
        variable = read_table('Variable')
        info_vars = variable[variable['fk_variable_dataset'] == id]

        metadata = __generate_metadata_variables_common(standard)
        
        list_id_var = info_vars['id'].tolist()
        
        for id_var in list_id_var:
            var = info_vars[info_vars['id'] == id_var]
            metadata.append(__generate_metadata_variable_count(var))
        
        if standard:
            for id_var in list_id_var:
                var = info_vars[info_vars['id'] == id_var]
                metadata.append(__generate_metadata_variable_rate(var))

        return metadata
    except:
        raise

def __parse_list_values(x, delim=','):
    if x.iloc[0] is None:
        return ['']
    else:
        list_values = x.iloc[0].split(delim)
        return [x.strip() for x in list_values]

def generate_metadata(id):
    """Generate a medata dictionary for a dataset."""
    try:
        dataset = read_table('Dataset') # if tables is None else tables.dataset
        info = dataset[dataset['id'] == id]
        standard = info['standard'].iloc[0] == 1
        
        return {
            'title': info['title'].iloc[0],
            'date': info['date_updated'].iloc[0],
            'sources': __generate_sources(info),
            'categories': __parse_list_values(info['categories']),
            'tags': __parse_list_values(info['tags']),
            'unit': info['unit'].iloc[0],
            'agegroup': info['age_group'].iloc[0],
            'timeperiod': __generate_time_period(info),
            'variables': __generate_metadata_variables(id, standard),
            'description': info['description'].iloc[0],
            'notes': __parse_list_values(info['notes'], '|')
        }
    except:
        raise