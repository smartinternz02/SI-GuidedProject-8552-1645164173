import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "C-URb26CyXeEajaBU3pSi8jZGDwGrA2Vl6eexPg9Fseo"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Demo2.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    #min max scaling
    min1=[290.0, 92.0, 1.0, 1.0, 1.0, 6.8, 0.0]
    max1=[340.0, 120.0, 5.0, 5.0, 5.0, 9.92, 1.0]
    k= [float(x) for x in request.form.values()]
    p=[]
    for i in range(7):
        l=(k[i]-min1[i])/(max1[i]-min1[i])
        p.append(l)
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring ={"input_data": [{"field": [['GRE Score', 'TOEFL Score', 'University Rating','SOP','LOR','CGPA','Research']],
                                       "values": [p]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/c5c34039-aea8-439b-adf1-7985c9e23976/predictions?version=2022-03-04', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    pred = response_scoring.json()

    output = pred['predictions'][0]['values'][0][0]
    if(output==False):
        return render_template('noChance.html', prediction_text='You Dont have a chance')
    else:
        return render_template('chance.html', prediction_text='You have a chance')
if __name__ == "__main__":
    app.run(debug=True)
