from util.database.dbread import read_table

def __generate_readme_variables_common(standard):
    """Return readme text for common variables."""
    readme = "- year (int): Data year.\r\n" +\
        "- id (int): Location identifier.\r\n" +\
        "- fips (int): Federal Information Processing Standard (FIPS) code.\r\n" +\
        "- county (str): County name.\r\n" +\
        "- region (str): Region of a county; Northern minus Cook, Northern - Cook, Central, or Southern.\r\n" +\
        "- community_type (str): Categorization based on the proportion of rural area in a county; Completely Rural (rural 100%), Mostly rural (rural >50%), Mostly urban (rural <50%), or Completely urban (rural 0%).\r\n" +\
        "- percent_rural (float): Percentage of rural area in a county.\r\n"
    
    if standard:
        readme += "- population (float): Population estimate.\n"
    return readme

def __generate_readme_variable_count(var):
    try:
        """Generate readme text for each count variable."""
        name = var['name'].iloc[0]
        definition = var['definition'].iloc[0]
        
        return f"- {name} (int): {definition}\r\n"
    except:
        print("failing to generate variable count")

def __generate_readme_variable_rate(var):
    """Generate readme text for each rate variable."""
    try:
        typerate = var['fk_variable_typerate'].iloc[0]
        dict_rate = {
            1: 'per 100,000',
            2: 'per cent'
        }

        if typerate in dict_rate.keys():
            name = var['name'].iloc[0]
            return f"- {name}_rate (float): Rate for '{name}' {dict_rate[typerate]}\r\n"
        else:
            return ''
    except:
        raise

def __generate_readme_variables(id, standard):
    """Generate readme text for variables."""
    try:
        variable = read_table('Variable')
        info_vars = variable[variable['fk_variable_dataset'] == id]

        readme = "\r\nVARIABLES\r\n"
        readme += __generate_readme_variables_common(standard)
        
        list_id_var = info_vars['id'].tolist()
        for id_var in list_id_var:
            var = info_vars[info_vars['id'] == id_var]
            readme += __generate_readme_variable_count(var)
        
        if standard:
            for id_var in list_id_var:
                var = info_vars[info_vars['id'] == id_var]
                readme += __generate_readme_variable_rate(var)

        return readme
    except:
        raise

def __generate_notes(notes):
    try:
        notes = notes.split('|')

        readme = "\r\nNOTES\r\n"
        for note in notes:
            readme += f'- {note}\r\n'
        
        return readme
    except:
        raise

def generate_readme(id):
    """Generate readme text for a dataset."""
    try:
        dataset = read_table('Dataset')
        info = dataset[dataset['id'] == id]
        standard = info['standard'].iloc[0] == 1

        title = info['title'].iloc[0]
        date_updated = info['date_updated'].iloc[0]
        source = info['source'].iloc[0]
        year_type = info['year_type'].iloc[0]
        year_min = int(info['year_min'].iloc[0])
        year_max = int(info['year_max'].iloc[0])
        age_group = info['age_group'].iloc[0]
        description = info['description'].iloc[0]
        notes = info['notes'].iloc[0]

        readme = f"TITLE: {title}\r\n"
        readme += f"DATE UPDATED: {date_updated}\r\n"
        readme += f"SOURCE: {source}\r\n"
        readme += f"TIME PERIOD: {year_min}-{year_max} ({year_type})\r\n"
        readme += f"AGE GROUP: {age_group}\r\n"
        readme += f"DESCRIPTION: {description}\r\n"
        readme += __generate_readme_variables(id, standard)
        if notes is not None:
            readme += __generate_notes(notes)

        return readme
    except:
        print(readme)
        raise