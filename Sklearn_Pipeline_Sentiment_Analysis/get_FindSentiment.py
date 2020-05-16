#from flask import Flask, render_template, request, redirect, url_for
import flask
from joblib import load
from sklearn.ensemble import RandomForestClassifier
import json
from flask import Flask,request,Response, jsonify
application = Flask(__name__)

pipeline = load("text_classification_spyder.joblib")


def readRequest(text):
    #print("read request is working")
    label = 0
    dictionary = {}
    label  = pipeline.predict(text)[0]
    if label == 0:
        dictionary.update({"Sentiment of tweet is": "Positive"})
        
    else:
        dictionary.update({"Sentiment of tweet is": "Negative"})
        
    return dictionary
    
    
    
## Define HomePage
#@app.route('/')
#def home():
#    return render_template('home.html')


#http://192.168.68.104:9052/SentimentAnalysis?input=this is first tweet
@application.route('/SentimentAnalysis', methods=['POST', 'GET'])
def SentimentAnalysis():
    #param = request.json
    param=(request.args.get('input',None))
    text = list(param)
    #print(text)
    #text = 'i am done'
    
    #text = list(text)
    rt = readRequest(text)
    ##js=json.dumps(rt)
    return jsonify(rt)

  
#@app.route('/', methods=['POST', 'GET'])
#def get_data():
#    param = request.json
#    text = param['body']
#    text = list(text)
#    return redirect(url_for('success', name=text))

  
#@app.route('/success/<name>')
#def success(name):
#    return "<xmp>" + str(requestResults(name)) + " </xmp> "


#if __name__ == '__main__' :
#    app.run(debug=True)
    
if __name__ == '__main__':
   application.run(host="0.0.0.0",port=9052,debug=False)