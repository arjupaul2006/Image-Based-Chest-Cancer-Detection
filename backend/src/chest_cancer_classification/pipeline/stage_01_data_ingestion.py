from src.chest_cancer_classification.config.configuration import ConfigurationManager
from src.chest_cancer_classification.components.data_ingestion import DataIngestion
from exception import CustomeException
import sys
from logger import logging

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            data_ingestion_config = ConfigurationManager().get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.download_data()
            data_ingestion.unzip_and_clean()

        except Exception as e:
            raise CustomeException(e, sys)


if __name__ == "__main__":
    try:
            logging.info(f">>>>> stage {STAGE_NAME} started <<<<<")
            obj = DataIngestionPipeline()
            obj.main()
            logging.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
    except Exception as e:
        raise CustomeException(e, sys)