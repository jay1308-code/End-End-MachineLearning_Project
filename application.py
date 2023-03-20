from flask import Flask

application = Flask(__name__)
app = application


@app.route("/",methods=["GET","POST"])
def index():
    return "Starting Of End To End Machine Learning Project!!!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")    