import pandas as pd
import json
import sys
import os
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.cofig_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.model_profile import Profile
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
class DataValidation:
    
    def __init__(self,data_validation_config:DataValidationConfig,
                  data_ingestion_artifact:DataIngestionArtifacts  ) -> None:

        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact_config = data_ingestion_artifact
        
    def is_train_test_file_exist(self)->bool:
        try:
            logging.info("Checking if training and testing file is available")
            is_train_file_exist = False
            is_test_file_exist = False
            train_file_path = self.data_ingestion_artifact_config.train_file_path
            test_file_path = self.data_ingestion_artifact_config.test_file_path

            is_train_file_exist =  os.path.exists(train_file_path)
            is_test_file_exist =  os.path.exists(test_file_path)

            is_available = is_train_file_exist and is_test_file_exist
            logging.info(f"Is train and test file available ? -> [{is_available}]")

            if not is_available:
                train_file_path = self.data_ingestion_artifact_config.train_file_path
                test_file_path = self.data_ingestion_artifact_config.test_file_path
                message  = f"Training file :[{train_file_path}] or Testing file :[{test_file_path}]" \
                    "is not present"
                logging.info(message)
                raise Exception(message)
            return is_available

        except Exception as e:
            raise HousingException(e,sys)

    def validate_dataset_schema(self)->bool:
        try:
            Validation_status =False
            #Assigment validation training and testing dataset using schema file
            # number of column
            # check the value of ocean proximity
            # check column names
            # acceptable values

            Validation_status = True 
            return Validation_status   
        except Exception as e:
            raise HousingException(e,sys)

    def get_train_and_test_df(self):
        try:

            train_df = pd.read_csv(self.data_ingestion_artifact_config.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact_config.test_file_path)

            return train_df,test_df
        except Exception as e:
            raise HousingException(e,sys)




    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df,test_df = self.get_train_and_test_df()
            
            # To Calculate the difference
            profile.calculate(train_df,test_df)
            
            # To save the report
            report = json.loads(profile.json())
            report_file_path =self.data_validation_config.report_file_path
            report_dir  = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)
            with open(report_file_path,"w") as report_file:
                json.dump(report,report_file,indent=6)

            return report    

        except Exception as e:
            raise HousingException(e,sys)

    def save_data_drift_page_report(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)
            report_page_file_path =self.data_validation_config.report_page_file_path
            report_page_file_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_file_dir,exist_ok=True)
            dashboard.save(report_page_file_path)

        except Exception as e:
            raise HousingException(e,sys)

    def is_data_drift_found(self):
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_page_report()

            return True
        except Exception as e:
            raise HousingException(e,sys)


    def initiate_data_validation(self)->DataValidationArtifacts:
        try:
            self.is_train_test_file_exist()
            self.validate_dataset_schema()  
            self.is_data_drift_found() 

            data_validation = DataValidationArtifacts(schema_file_path=self.data_validation_config.schema_file_path,
            report_file_path=self.data_validation_config.report_file_path,
            report_page_file_path=self.data_validation_config.report_page_file_path,
            is_validated=True,
            message="Data VAlidation performed successfully")

            logging.info(f"DataVAlidation Artifacts :{[data_validation]}")

        except Exception as e:
            raise HousingException(e,sys)
