import os
from datetime import datetime

ROOT_DIR = os.getcwd() # to get current working dir

CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

# training_pipeline variables:
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"

# DataIngestion related variable
DATA_INGESTION_CONFIG_KEY ="data_ingestion_config"
DATA_INGESTION_RAW_DATA_DIR_KEY="raw_data_dir"
DATA_INGESTION_DOWNLOAD_URL_KEY="dataset_download_url"
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY="tgz_download_dir"
DATA_INGESTION_INGESTED_TRAIN_DIR="ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DIR="ingested_test_dir"
DATA_INGESTION_INGESTED_DIR ="ingested_dir"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"

# DATA VALIDATION RELATED CONSTANTS
DATA_VALIDATION_CONFIG_KEY ="data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY ="schema_file_path"
DATA_VALIDATION_ARTIFACTS_DIR_NAME = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_path_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY ="report_page_file_name"
