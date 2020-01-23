import json

from database.main import update_date_updated
from dataset.generate_data import generate_data
from dataset.generate_metadata import generate_metadata
from dataset.generate_readme import generate_readme

def create_data_csv(id):
    """Return the data for the specified dataset in CSV."""
    try:
        csv = generate_data(id).to_csv(index=False)
        update_date_updated(id)
        return csv
    except:
        print("ERROR: Failed to create data CSV!")
        raise

def create_metadata_json(id):
    """Return the metadata for the specified dataset in JSON."""
    try:
        return json.dumps(generate_metadata(id))
    except:
        print("ERROR: Failed to create metadata JSON!")
        raise

def create_readme_txt(id):
    """Return the REAMDE text for the specified dataset."""
    try:
        txt = "This dataset is prepared and published by " +\
            "Illinois Criminal Justice Information Authority (ICJIA). " +\
            "Visit http://icjia.state.il.us to learn more about ICJIA.\r\n\r\n"
        txt += generate_readme(id)
        
        return txt
    except:
        print("ERROR: Failed to create README text!")
        raise