from flask import Flask,request
import os
import time
import requests
import json
import base64
app = Flask(__name__)
SK_ESTOKEN=''

@app.route('/')
def hello_world():
   return 'Hello World'
   
@app.route('/getbal',methods=['GET'])
def getbal():
   addr=request.args.get('addr')
   url="https://api.etherscan.io/api?module=account&action=balance&address="+addr+"&tag=latest&apikey="+SK_ESTOKEN
   res=requests.get(url)
   return res.text

@app.route('/getprice',methods=['GET'])
def getprice():
   url="https://api.etherscan.io/api?module=stats&action=ethprice&apikey="+SK_ESTOKEN
   res=requests.get(url)
   return res.text

@app.route('/geturl',methods=['GET'])
def getprice():
   tourl=request.args.get('tourl')
   url=str(base64.b64decode(tourl), 'utf-8')
   res=requests.get(url)
   return res.text
   
if __name__ == '__main__':
   SK_ESTOKEN= os.environ.get('SK_ESTOKEN')
   app.run('0.0.0.0',82,True)
