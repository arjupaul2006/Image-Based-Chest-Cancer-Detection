from src.chest_cancer_classification.constants import CONFIG_YAML_PATH, PARAM_YAML_FILE
from src.chest_cancer_classification.utils.common import read_yaml_file, create_directories
from src.chest_cancer_classification.entity.config_entity import DataIngestionConfig

class ConfigurationManager:
    def __init__(self, config_file_path=CONFIG_YAML_PATH, params_file_path=PARAM_YAML_FILE):
        self.config = read_yaml_file(config_file_path)
        self.params = read_yaml_file(params_file_path)
        create_directories([self.config.artifact_dir])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.rootdir])

        data_ingestion_config = DataIngestionConfig(
            root_dir = config.rootdir,
            source_url = config.source_url,
            local_data_file = config.local_data_file,
            unzip_dir = config.unzip_dir
        )

        return data_ingestion_config