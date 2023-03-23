import yaml
from housing.exception import HousingException
import os,sys

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
