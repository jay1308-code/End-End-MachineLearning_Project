from housing.entity.cofig_entity import DataIngestionConfig,DataValidationConfig,DatTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig,TrainingPipelineConfig
from housing.util.util import read_yaml_file
from housing.constant import *
from housing.logger import logging
from housing.exception import HousingException
import sys
import os





class Configuration:

    def __init__(self,
        config_file_path:str=CONFIG_FILE_PATH,
        current_time_stamp:str=CURRENT_TIME_STAMP)->None:
        try:
            self.config_info = read_yaml_file(file_path = config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
            

        except Exception as e:
            raise HousingException(e,sys) from e   
        

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_path = os.path.join(artifact_dir,DATA_INGESTION_INGESTED_DIR,self.time_stamp)
            
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            tgz_download_dir = os.path.join(
                data_ingestion_artifact_path,
                data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            )

            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            raw_data_dir = os.path.join(
                data_ingestion_artifact_path,
                data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]

            )

            ingested_data_dir = os.path.join(
                data_ingestion_artifact_path,
                data_ingestion_info[DATA_INGESTION_INGESTED_DIR]
            )

            ingested_train_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_TRAIN_DIR]
            )

            ingested_test_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_TEST_DIR]
            )

            data_ingestion_config = DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                tgz_download_dir=tgz_download_dir,
                raw_data_dir=raw_data_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir
            )

            logging.info(f"Data Ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_validation_config(self)->DataValidationConfig:
        try:
            data_validation_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            artifact_dir = self.training_pipeline_config.artifact_dir

            data_validation_artifact_path = os.path.join(artifact_dir,
                                                        DATA_VALIDATION_ARTIFACTS_DIR_NAME,
                                                        self.time_stamp)

            schema_file_path =os.path.join(ROOT_DIR,
                                            CONFIG_DIR,
                                            data_validation_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
                                            )

            report_file_path  = os.path.join(data_validation_artifact_path,
                                            data_validation_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
                                            ) 

            report_file_page_path = os.path.join(data_validation_artifact_path,
                                                data_validation_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY]
                                                ) 

            data_validation_config =DataValidationConfig(schema_file_path=schema_file_path,
                                                            report_file_path=report_file_path,
                                                            report_page_file_path=report_file_page_path
                                                            )
            return data_validation_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_transformation_config(self)->DatTransformationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_transformation_artifact_path = os.path.join(artifact_dir,
                                                        DATA_TRANSFORMATION_ARTIFACT_DIR,
                                                        self.time_stamp
                                                        )

            data_transformation_config = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY] 
            add_bedroom_per_room = data_transformation_config[DATA_TRANSFORMATION_ADD_BADROOM_PER_ROOM_KEY]
            preprocessed_object_file_path = os.path.join(data_transformation_artifact_path,data_transformation_config[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],data_transformation_config[DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_PATH_KEY])
            transformed_train_dir=os.path.join(
                data_transformation_artifact_path,
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR_KEY],
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DATA_DIR_KEY]

            )

            transformed_test_dir = os.path.join(
                data_transformation_artifact_path,
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR_KEY],
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_TEST_DATA_DIR_KEY]

            )

            data_transformation_config = DatTransformationConfig(
                add_bedroom_per_room=add_bedroom_per_room,
                transformed_train_dir=transformed_train_dir,
                transformed_test_dir=transformed_test_dir,
                preprocessed_object_file_path=preprocessed_object_file_path,

                )
            logging.info(f"{'='*20} DataTransformation log Started {'='*20}")    
            logging.info(f"Data transformation config:[{data_transformation_config}]")    
            return data_transformation_config                                     
            
        except Exception as e:
            raise HousingException(e,sys)

    def get_model_trainer_config(self)->ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self)->ModelPusherConfig:
        pass

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir  = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipeline config : {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise HousingException(e,sys) from e