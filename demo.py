from housing.pipeline.pipeline import Pipeline 
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
import sys

def main():
    try:
        pipeline =Pipeline()
        pipeline.run_pipeline()


    except Exception as e:
        raise HousingException(e,sys)
          


if __name__ == '__main__':
    main()    
    