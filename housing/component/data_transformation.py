from housing.exception import HousingException
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts,DataTransformationArtifacts
from housing.entity.cofig_entity import DatTransformationConfig
import os,sys
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import  SimpleImputer
import pandas as pd
from housing.util.util import read_yaml_file,save_numpy_array,load_numpy_array,save_object,load_object,load_data
from housing.constant import *





class FeatureGenerator(BaseEstimator, TransformerMixin):

    def __init__(self, add_bedrooms_per_room=True,
                 total_rooms_ix=3,
                 population_ix=5,
                 households_ix=6,
                 total_bedrooms_ix=4, columns=None):
        """
        FeatureGenerator Initialization
        add_bedrooms_per_room: bool
        total_rooms_ix: int index number of total rooms columns
        population_ix: int index number of total population columns
        households_ix: int index number of  households columns
        total_bedrooms_ix: int index number of bedrooms columns
        """
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix = self.columns.index(COLUMN_POPULATION)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOM)

            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_ix = total_rooms_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
            self.total_bedrooms_ix = total_bedrooms_ix
        except Exception as e:
            raise HousingException(e, sys) from e

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            room_per_household = X[:, self.total_rooms_ix] / \
                                 X[:, self.households_ix]
            population_per_household = X[:, self.population_ix] / \
                                       X[:, self.households_ix]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / \
                                    X[:, self.total_rooms_ix]
                generated_feature = np.c_[
                    X, room_per_household, population_per_household, bedrooms_per_room]
            else:
                generated_feature = np.c_[
                    X, room_per_household, population_per_household]

            return generated_feature
        except Exception as e:
            raise HousingException(e, sys) from e

class DataTransformation:

    def __init__(self,
                data_ingestion_artifact:DataIngestionArtifacts,
                data_validation_artifact: DataValidationArtifacts,
                data_transformation_config: DatTransformationConfig) -> None:

        

        try:
            
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifacts = data_validation_artifact

        except Exception as e:
            raise HousingException(e,sys)


    

    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            schema_file_path =self.data_validation_artifacts.schema_file_path

            dataset_schema = read_yaml_file(schema_file_path)

            numerical_columns = dataset_schema[SCHEMA_NUMERICAL_COLUMN_KEY]

            categorical_columns = dataset_schema[SCHEMA_CATEGORICAL_COLUMN_KEY]

            # Pipelines for numerical and categorical data
            num_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("feature_genrator",FeatureGenerator(add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                columns=numerical_columns)),
                ("scaler",StandardScaler(with_mean=False))
            ])

            categorical_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("encoding",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))

            ])

            logging.info(f"Categorical Columns :[{categorical_columns}]")
            logging.info(f"Numerical Columns :[{numerical_columns}]")

            
            # Preprocessor
            preprocessor = ColumnTransformer([
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline",categorical_pipeline,categorical_columns)
            ])

            return preprocessor

        except Exception as e:
            raise HousingException(e,sys) from e      

    def initiate_data_transformation(self)->DataTransformationArtifacts:
        try:
            logging.info(f"Obtaining preprocessor object")
            preprocessor_obj = self.get_data_transformer_object()
            
            logging.info(f"Obtaining train and test file path")
            train_file_path = self.data_ingestion_artifact.train_file_path

            test_file_path = self.data_ingestion_artifact.test_file_path
            
            logging.info(f"Obtaining Schema file path")
            schema_file_path = self.data_validation_artifacts.schema_file_path
            
            schema = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[SCHEMA_TARGET_COLUMN_KEY]
            
            
            logging.info(f"Loading train and test file data as Dataframe")
            train_df = load_data(file_path=train_file_path,schema_path=schema_file_path)

            inputs_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            

            
            
            target_feature_train_df = train_df[target_column_name]

            test_df = load_data(file_path=test_file_path,schema_path=schema_file_path)
            
            logging.info(f"Splitting train and test data into input_feature and target_feature")
            
            inputs_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)

            target_feature_test_df = test_df[target_column_name]
            
            logging.info(f"Applying preprocessor object on training and testing data")
            input_feature_transformed_train_arr = preprocessor_obj.fit_transform(inputs_feature_train_df)
            input_feature_transformed_test_arr = preprocessor_obj.transform(inputs_feature_test_df)

            train_arr = np.c_[input_feature_transformed_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_transformed_test_arr,np.array(target_feature_test_df)]
            
            transformed_train_data_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_data_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_data_path = os.path.join(transformed_train_data_dir,train_file_name)
            transformed_test_data_path = os.path.join(transformed_test_data_dir,test_file_name)

            logging.info(f"Saving training and testing data in artifacts")
            save_numpy_array(file_path=transformed_train_data_path,array=train_arr)
            save_numpy_array(file_path=transformed_test_data_path,array=test_arr)

            preprocessor_file_path = self.data_transformation_config.preprocessed_object_file_path
            
            logging.info(f"Saving the preprocessor object")
            save_object(file_path=preprocessor_file_path,object=preprocessor_obj)

            data_transform_artifacts = DataTransformationArtifacts(
                message="DataTransformation Completed",
                is_transformed=True,
                transformed_train_file_path=transformed_train_data_path,
                transformed_test_file_path=transformed_test_data_path,
                preprocessed_object_file_path=preprocessor_file_path 

                
        
            )
            logging.info(f"DataTransformation Artifacts:[{data_transform_artifacts}]")
            logging.info(f"{'='*20} Data Transformation log Completed {'='*20}\n\n")
            return data_transform_artifacts

        except Exception as e:
            raise HousingException(e,sys)

