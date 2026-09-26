from logger import logging
from exception import CustomeException
import sys
import os
import gdown
import zipfile
from src.chest_cancer_classification.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_data(self):
        """Downloads the data from the source URL and saves it to the local data file path."""
        try:
            dataset_url = self.config.source_url
            zip_file = self.config.local_data_file

            logging.info(f"Downloading file from :[{dataset_url}] into :[{zip_file}]")

            file_id = dataset_url.split('/')[-2]
            prefix = 'https://drive.google.com/uc?export=download&id='
            gdown.download(prefix + file_id, zip_file, quiet=False)

            logging.info(f"Downloaded file from :[{dataset_url}] into :[{zip_file}]")

        except Exception as e:
            raise CustomException(e, sys)

    def unzip_and_clean(self):
        try:
            zip_file = self.config.local_data_file
            unzip_dir = self.config.unzip_dir

            os.makedirs(unzip_dir, exist_ok=True)

            logging.info(f"Unzipping file :[{zip_file}] into :[{unzip_dir}]")
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)
            logging.info(f"Unzipped file :[{zip_file}] into :[{unzip_dir}]")

            os.remove(zip_file)
            logging.info(f"Removed zip file :[{zip_file}]")
        except Exception as e:
            raise CustomeException(e, sys)