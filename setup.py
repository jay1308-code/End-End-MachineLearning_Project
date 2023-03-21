from setuptools import setup
from typing import List

PROJECT_NAME = "HOUSING-PREDICTOR"
PROJECT_VERSION = "0.0.1"
AUTHOR = "JAY"
DESCRIPTIONS = "SECOND END TO END ML PROJECT"
PACKAGES = ["housing"]
REQUIREMENT_FILE_NAME = 'requirements.txt'

def get_requirements_list()->List[str]:
    """
    This Function going to return the list of the requirements 
    mentioned in the requirements.txt file

    Returns:
        List[str]: return the list of the requirements mentioned in the requirements.txt
        it will be str data in the list
    """

    with open(REQUIREMENT_FILE_NAME) as requirements_file:
        return requirements_file.readlines()



setup(
    name = PROJECT_NAME,
    version=PROJECT_VERSION,
    author=AUTHOR,
    description = DESCRIPTIONS,
    packages=PACKAGES,
    install_requires = get_requirements_list(),

)


