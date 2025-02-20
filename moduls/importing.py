from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd


# Initialize the Kaggle API
api = KaggleApi()
api.authenticate()  # Authenticate using the Kaggle API key stored in ~/.kaggle/kaggle.json


def importing(dataset_name, download_path):
    """
    Downloads a dataset from Kaggle and extracts it to the specified directory.

    Parameters:
        dataset_name (str): The Kaggle dataset identifier (e.g., 'muthuj7/weather-dataset').
        download_path (str): The local path where the dataset should be stored.

    Returns:
        None
    """

    # Download and unzip the dataset
    api.dataset_download_files(dataset_name, path=download_path, unzip=True)


def csv_reader(path):
    # 🔹 Загрузка датасета (замени на свой путь)
    print('Importing...')
    df = pd.read_csv(path)

    return df

