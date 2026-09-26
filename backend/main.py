from logger import logging
from exception import CustomeException
import sys
from src.chest_cancer_classification.pipeline.stage_01_data_ingestion import DataIngestionPipeline


STAGE_NAME = "Data Ingestion Stage"

if __name__ == "__main__":
     try:
        logging.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logging.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
     except Exception as e:
        raise CustomeException(e, sys)