from flask import Flask
import sys
from housing.logger import logging
from housing.exception import HousingException
application = Flask(__name__)
app = application


@app.route("/",methods=["GET","POST"])
def index():
    try:
        0/0
    except Exception as e:
        housing  = HousingException(e,sys)
        logging.info(housing.error_message)
        logging.info("we are testing the Exception module")


    
    return "Starting Of End To End Machine Learning Project!!!"

if __name__ == "__main__":
    app.run()    