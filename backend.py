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
        return "Provide a username"
    else:
        user_info = get_user_info(request.args.get("username"))
        if not user_info:
            print colored("[ERROR]", "red"), "Something went wrong while crawling data from Instagram"
            return "Invalid username or maybe this account is private?"
        else:
            print colored("[OK]", "green"), "User's data crawler"
            # return jsonify(user_info)
            try:
                features = make_user_features(user_info)
                print colored("[OK]", "green"), features
            except:
                print colored("[ERROR]", "red"), "Error while processing features"
                return "ERROR"

            try:
                predictions = user_predict(features)
                print colored("[OK]", "green"), "Predictins: ", predictions            
            except:
                print colored("[ERROR]", "red"), "Predicting don't work correctly :("

            return "OK"

if __name__ == "__main__":
    app.run()