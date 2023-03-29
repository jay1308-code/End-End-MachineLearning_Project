from collections import namedtuple

# DataIngestionConfig:
# 1 : Download Url
# 2 : Download Folder(Compressed file)
# 3: Extract raw file(extracted file)
# 4 : Train dataset folder
# 5 : Test dataset folder

DataIngestionConfig = namedtuple("DataIngestionConfig",
                                ["dataset_download_url"
                                ,"tgz_download_dir",
                                "raw_data_dir",
                                "ingested_train_dir",
                                "ingested_test_dir"]
                                                    )

# DataValidationConfig:
# 1 : Schema file path (who contain the all info related how many numbers of columns,file formate etc)                                                

DataValidationConfig = namedtuple("DataValidationConfig",["schema_file_path","report_page_file_path","report_file_path"])

# DataTransformationConfig:
# 1: Adding some bedrooms in the data 
# 2 : Transformed train data dir path
# 3 : Transformed test data dir path 
# 4 : preprocessed obj data file path

DatTransformationConfig = namedtuple("DatTransformationConfig",
                                    ["add_bedroom_per_room",
                                    "transformed_train_dir",
                                    "transformed_test_dir",
                                    "preprocessed_object_file_path"])

# ModelTrainerConfig:
# 1: giving the file path where the train model will going to save
# 2: the base accuracy

ModelTrainerConfig = namedtuple("ModelTraningConfig",["train_model_file_path","base_accuracy"])

# ModelEvaluationConfig:
# 1: model evaluation info
# 2 : timestamp

ModelEvaluationConfig = namedtuple("ModelEvaluationConfig",["model_evaluation_file_path","time_stamp"])

# ModelPusherConfig:
# 1: final model dir path
 
ModelPusherConfig  = namedtuple("ModelPusherConfig",["export_dir_path"])

# TrainingPipelineConfig:
# 1: gave a path where all the artifacts will going to saved

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig",["artifact_dir"])
