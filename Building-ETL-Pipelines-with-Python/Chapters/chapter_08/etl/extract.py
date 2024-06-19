# import dependent modules
import pandas as pd

# extract data
def extract_data(filepath: object, select_cols: list, rename_cols: dict) -> object:
    """
       Simple Extract Function in Python with Error Handling
       :param filepath: str, file path to CSV data
       :output: pandas dataframe, extracted from CSV data
    """
    try:
        # Read the CSV file and store it in a dataframe
        df = pd.read_csv(filepath)
        df = df[select_cols]
        df = df.rename(columns={rename_cols})

    # Handle exception if any of the files are missing
    except FileNotFoundError as e:
        print(f"Error: {e}")

    # Handle any other exceptions
    except Exception as e:
        print(f"Error: {e}")

    return df
