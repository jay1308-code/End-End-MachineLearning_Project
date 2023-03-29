from collections import namedtuple

DataIngestionArtifacts = namedtuple("DataIngestionArtifacts",
                                    ["train_file_path",
                                    "test_file_path",
                                    "is_ingested",
                                    "message"]
                                                )
                                                
DataValidationArtifacts = namedtuple("DataValidationArtifacts",["schema_file_path",
                                        "report_file_path",
                                        "report_page_file_path",
                                        "is_validated",
                                        "message"]
                                                    )                                                