from flask import Flask
from flask import request
import pickle
from env_backend import *
from flask import Response, jsonify
from termcolor import colored

app = Flask(__name__)

@app.route("/")
def hello():
    return "<a href='predict?username=kugusha'>Predict!!11</a>"

@app.route("/predict")
def predict():
    print "Args:", request.args
    if not request.args.get("username"):
        print colored("[ERROR]", "red"), "No username"
        return jsonify({"error" : True, "text" : "No username"})
    else:
        user_info = get_user_info(request.args.get("username"))
        if not user_info:
            print colored("[ERROR]", "red"), "Something went wrong while crawling data from Instagram"
            return jsonify({"error" : True, "text" : "Invalid username"})
        else:
            print colored("[OK]", "green"), "User's data crawled"
            # print colored("[INFO]", "blue"), user_info

            try:
                features = make_user_features(user_info)
                print colored("[OK]", "green"), features
            except:
                print colored("[ERROR]", "red"), "Error while processing features"
                return jsonify({"error" : True, "text" : "Error with feature processing"})

            try:
                predictions = user_predict(features)
                print colored("[OK]", "green"), "Predictins: ", predictions            
                return jsonify(predictions)
            except:
                print colored("[ERROR]", "red"), "Predicting don't work correctly :("
                return jsonify({"error" : True, "text" : "Error with predicting"})

if __name__ == "__main__":
    app.run()