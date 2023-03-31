from housing.pipeline.pipeline import Pipeline 
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
import sys
from housing.component.data_transformation import DataTransformation

def main():
    try:
        pipeline =Pipeline()
        pipeline.run_pipeline()
        # data_transformation = Configuration().get_data_transformation_config()
        # print(data_transformation)
        # schema_file_path = r"C:\Users\Lenovo\Desktop\END-END-MACHINELEARNINGPROJECT\End-End-MachineLearning_Project\config\schema.yaml"
        # file_path = r"C:\Users\Lenovo\Desktop\END-END-MACHINELEARNINGPROJECT\End-End-MachineLearning_Project\housing\artifact\ingested_dir\2023-03-30_12-12-33\ingested_data\train\housing.csv"
        # df = DataTransformation.load_data(file_path=file_path,schema_path=schema_file_path)
        # print(df.columns)
        # print(df.dtypes)

    except Exception as e:
        raise HousingException(e,sys)
          


if __name__ == '__main__':
    main()    
    