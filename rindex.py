from flask import Flask
import os
import requests
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
   SK_CORPID = os.environ.get('SK_CORPID')
   return 'Hello World'+SK_CORPID
def getbal():
   SK_ESTOKEN = os.environ.get('SK_ESTOKEN')
   url="https://api.etherscan.io/api?module=account&action=balance&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&tag=latest&apikey="+SK_ESTOKEN
   res=requests.get(url)
   rjson=res.json()
   return 'bal'+rjson['result']
   
if __name__ == '__main__':
   app.run('0.0.0.0',82,True)
