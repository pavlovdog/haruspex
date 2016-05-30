from flask import Flask
from flask import request
import pickle
from env_backend import 

app = Flask(__name__)

@app.route("/")
def hello():
	return "<a href='predict'>Predict!!11</a>"

@app.route("/predict")
def predict():
	print "Args:", request.args
	return "MAGICCCC!!!"

if __name__ == "__main__":
	app.run()