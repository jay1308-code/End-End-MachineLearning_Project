from housing.entity.cofig_entity import DataIngestionConfig
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifacts
import sys,os
import tarfile
from  six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20} Data Ingestion log started.{'='*20}")
            self.data_ingestion_config = data_ingestion_config
            
            
        except Exception as e:
            raise HousingException(e,sys) from e

    def download_housing_data(self)->str:
        """
        Download the data from url and return the trz file path
        Returns:
            str: trz file path
        """
        try:
            
            # extracting the remote url for download the dataset
            download_url = self.data_ingestion_config.dataset_download_url

            # folder where the dataset will load
            tgz_download = self.data_ingestion_config.tgz_download_dir

            if os.path.exists(tgz_download):
                os.path.remove(tgz_download)

            os.makedirs(tgz_download,exist_ok =True)

            # extracting the file name form url
            housing_file_name = os.path.basename(download_url)

            # complete path for download the ZIP file
            tgz_file_path = os.path.join(tgz_download,housing_file_name)
            
            logging.info(f"Downloading file from :[{download_url}] into :[{tgz_file_path}]")
            # downloading the  url into the trz_file_path
            urllib.request.urlretrieve(download_url,tgz_file_path)

            logging.info(f"File :[{tgz_file_path}] has been downloaded successfully")

            return tgz_file_path

        except Exception as e:
            raise HousingException(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.path.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok =True)
            
            logging.info(f"Extracting file : [{tgz_file_path}] to dir : [{raw_data_dir}]")

            with tarfile.open(tgz_file_path) as housing_tgz_file_path_obj :
                housing_tgz_file_path_obj.extractall(path=raw_data_dir)

            logging.info(f"Extraction completed")  

        except Exception as e:
            raise HousingException(e,sys) from e

    def split_data_as_train_test(self):
        raw_data_dir = self.data_ingestion_config.raw_data_dir
        
        file_name = os.listdir(raw_data_dir)[0]

        housing_file_path = os.path.join(raw_data_dir,file_name)
        logging.info(f"Raeding csv file : [{housing_file_path}]")

        housing_file_dataframe = pd.read_csv(housing_file_path)

        housing_file_dataframe["income_cat"] = pd.cut(
            housing_file_dataframe["median_income"],
            bins=[0.0,1.5,3.0,4.5,6.0,np.inf],
            labels=[1,2,3,4,5]
        )
        
        logging.info(f"Spliting data into train test")
        strat_train_set = None
        strat_test_set = None

        split  = StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
        
        for train_index,test_index in split.split(housing_file_dataframe,housing_file_dataframe["income_cat"]):
            strat_train_set = housing_file_dataframe.loc[train_index].drop(["income_cat"],axis=1)
            strat_test_set = housing_file_dataframe.loc[test_index].drop(["income_cat"],axis=1)

        train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
        test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name) 

        if strat_train_set is not None:
            os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok =True)
            logging.info(f"Exporting the Train data to :[{train_file_path}]")
            strat_train_set.to_csv(train_file_path)

        if strat_test_set is not None:
            os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok =True)
            logging.info(f"Exporting test data to : [{test_file_path}]")
            strat_test_set.to_csv(test_file_path)

        data_ingestion_artifact =DataIngestionArtifacts(
            train_file_path=train_file_path,
            test_file_path=test_file_path,
            is_ingested=True,
            message=f"Data ingestion completed successfully."
        )
        logging.info(f"Data ingestion Artifact :[{data_ingestion_artifact}]")
        return  data_ingestion_artifact  

    def initiate_data_ingestion(self)->DataIngestionArtifacts:
        try:
            tgz_file_path = self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise HousingException(e,sys)
    
    def __del__(self):
        logging.info(f"{'='*20} Data Ingestion Log  Completed.{'='*20} \n\n")
