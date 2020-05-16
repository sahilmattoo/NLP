from flask import Flask, render_template, request, redirect, url_for
import flask
from joblib import load
from sklearn.ensemble import RandomForestClassifier
import json
from flask import Flask,request,Response, jsonify
application = Flask(__name__)

#pipeline = load("text_classification_spyder.joblib")
pipeline = load("text_classification_spyder_Modified.joblib")


def readRequest(name):
    #print("read request is working")
    text = list(name)
    
    label = 0
    dictionary = {}
    label  = pipeline.predict(text)[0]
    if label == 0:
        dictionary.update({"Sentiment of tweet is": "Positive"})
        
    else:
        dictionary.update({"Sentiment of tweet is": "Negative"})
        
    return dictionary
    
    
    
## Define HomePage
@application.route('/')
def home():
    return render_template('home.html')

##http://192.168.68.106:9052/SentimentAnalysis
#@application.route('/SentimentAnalysis', methods=['POST'])
#def SentimentAnalysis():
#    #param = request.json
#    #text = param['body']
#    #print(text)
#    #text = 'i am done'
#    
#    text = list(text)
#    rt = readRequest(text)
#    ##js=json.dumps(rt)
#    return jsonify(rt)

  
@application.route('/', methods=['POST'])
def get_data():
    
#    param = request.json
#    text = param['body']
#    text = list(text)
    text = request.form['search']
    return redirect(url_for('success', name=text))

  
@application.route('/success/<name>')
def success(name):
    return "<xmp>" + str(readRequest(name)) + " </xmp> "


if __name__ == '__main__' :
    application.run(debug=True)
    
#if __name__ == '__main__':
#   application.run(host="0.0.0.0",port=9052,debug=False)
    
    
    
    




    