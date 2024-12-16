from flask import Flask,request
import os
import time
import requests
import json
app = Flask(__name__)

@app.route('/')

def hello_world():
   SK_CORPID = os.environ.get('SK_CORPID')
   return 'Hello World'+SK_CORPID

@app.route('/getbal',methods=['GET'])
def getbal():
   SK_ESTOKEN = os.environ.get('SK_ESTOKEN')
   addr=request.args.get('addr')
   url="https://api.etherscan.io/api?module=account&action=balance&address="+addr+"&tag=latest&apikey="+SK_ESTOKEN
   res=requests.get(url)
   rjson=res.json()
   return 'bal'+rjson['result']
   
if __name__ == '__main__':
   app.run('0.0.0.0',82,True)
