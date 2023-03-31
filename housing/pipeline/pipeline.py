from housing.config.configuration import Configuration
from housing.logger import logging
from housing.exception import HousingException
import os,sys
from housing.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts,DataTransformationArtifacts
from housing.entity.cofig_entity import DataIngestionConfig
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation

class Pipeline:

    def __init__(self,config:Configuration=Configuration()) -> None:
        try:
            self.config = config
        except  Exception as e:
            raise HousingException(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifacts:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise HousingException(e,sys)
            
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifacts)->DataValidationArtifacts:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                            data_ingestion_artifact=data_ingestion_artifact)

            return data_validation.initiate_data_validation()                                    

        except Exception as e:
            raise HousingException(e,sys)  

    def start_data_transformation(self,data_ingestion_artifacts:DataIngestionArtifacts,data_validation_artifacts:DataValidationArtifacts)->DataTransformationArtifacts:
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifacts,
                                                        data_validation_artifact=data_validation_artifacts,
                                                        data_transformation_config=self.config.get_data_transformation_config())

            return data_transformation.initiate_data_transformation()

        except Exception as e:
            raise HousingException(e,sys)

        
    def start_model_trainer(self):
        pass
    def start_model_evaluation(self):
        pass
    def start_model_pusher(self):
        pass       

    def run_pipeline(self):
        try:
            # data ingestion
            data_ingestion = self.start_data_ingestion()
            # data validation
            data_validation = self.start_data_validation(data_ingestion_artifact=data_ingestion) 
            # data transformation
            data_transformation = self.start_data_transformation(data_ingestion_artifacts=data_ingestion,
                                                                data_validation_artifacts=data_validation)  
        except Exception as e:
            raise HousingException(e,sys)         



