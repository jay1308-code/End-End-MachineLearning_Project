import yaml
from housing.exception import HousingException
import os,sys
import numpy as np
import dill
import pandas as pd
from housing.constant import *

def read_yaml_file(file_path:str)->dict:
    """
    Read the YAML file 

    Args:
        file_path (str):file path

    Raises:
        e: _description_

    Returns:
        dict: return the YAML contain in dict
    """
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:     
        raise HousingException(e,sys) from e  


def save_numpy_array(file_path:str,array:np.array):

    """Save the data in array to given location

    Args:
        file_path (str): str file path where the data will be save
        array (np.array): numpy array 
    """
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)

    except Exception as e:
        raise HousingException(e,sys)        

def load_numpy_array(file_path:str)->np.array:
    """load the data from the file path

    Args:
        file_path (str): file path to array stored

    Returns:
        _type_: np.array
    """
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj) 

    except Exception as e:
        raise HousingException(e,sys)        

def save_object(file_path:str,object):
    """ Save the object 

    Args:
        file_path (str): Location where the object will save
        object (_type_): object which will going save in given location

    Raises:
        HousingException: _description_
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_object:
            dill.dump(object,file_object)

    except Exception as e:
        raise HousingException(e,sys)  

def load_object(file_path:str):
    try:
        with open(file_path,"rb") as file_object:
            return dill.load(file_object)

    except Exception as e:
        raise HousingException(e,sys)    



def load_data(file_path:str,schema_path:str)->pd.DataFrame:

        try:
            dataset_schema = read_yaml_file(schema_path)

            schema_column = dataset_schema[SCHEMA_COLUMN_KEY]

            dataframe = pd.read_csv(file_path)
            dataframe = dataframe.drop(["Unnamed: 0"],axis=1)

            for column in dataframe.columns:
                if column in list(schema_column.keys()):
                    dataframe[column].astype(schema_column[column])
                else:
                    error_message = f"Columns: [{column}] is not in the schema"
                    print(error_message)

            return dataframe        

        except Exception as e:
            raise HousingException(e,sys)

