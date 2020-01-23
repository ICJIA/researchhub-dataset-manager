
import os

def delete_file(dirname, filename):
    """Delete comma-separated values file.

    Args:
        df (pandas DataFrame): Data input.
        dirname (str): Directory name to save a output file.
        filename (str): Output file name.
    
    """
    path = f'{dirname}/{filename}.csv'
    if os.path.isfile(path):
        os.remove(path)
    else:
        print(f"NOTE: '{filename}.csv' file not found in '{dirname}' directory.")

def write_file(df, dirname, filename):
    """Create comma-separated values file from a pandas DataFrame.

    Args:
        df (pandas DataFrame): Data input.
        dirname (str): Directory name to save a output file.
        filename (str): Output file name.

    """
    path = f'{dirname}/{filename}.csv'
    df.to_csv(path, index=False)