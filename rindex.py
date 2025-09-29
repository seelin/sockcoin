from flask import Flask,request
import os
import time
import requests
import json
import base64
import redis
import logging

app = Flask(__name__)
SK_ESTOKEN=''
SK_CMCKEY=''
SK_EXCKEY=''
ES_HOST = "https://api.etherscan.io/v2/api"

def is_base64(s):
    try:
        if isinstance(s, str):
            s = s.encode()
        base64.b64decode(s, validate=True)
        return True
    except base64.binascii.Error:
        return False
       
@app.route('/')
def hello_world():
   chainid=request.args.get('chainid','1')
   return f'Hello World,{chainid}'
   
@app.route('/getbal',methods=['GET'])
def getbal():
   addr=request.args.get('addr')
   if not is_base64(addr): return 'addr error'
   addr=str(base64.b64decode(addr), 'utf-8')
   chainid=request.args.get('chainid','1')
   url=ES_HOST+"?chainid="+chainid+"&module=account&action=balance&address="+addr+"&tag=latest&apikey="+SK_ESTOKEN
   res=requests.get(url)
   return res.text
   
@app.route('/gettkbal',methods=['GET'])
def gettkbal():
   addr=request.args.get('addr')
   if not is_base64(addr): return 'addr error'
   addr=str(base64.b64decode(addr), 'utf-8')
   tkaddr=request.args.get('tkaddr')
   if not is_base64(tkaddr): return 'tkaddr error'
   tkaddr=str(base64.b64decode(tkaddr), 'utf-8')
   chainid=request.args.get('chainid','1')
   url=ES_HOST+"?chainid="+chainid+"&module=account&action=tokenbalance&contractaddress="+tkaddr+"&address="+addr+"&tag=latest&apikey="+SK_ESTOKEN
   res=requests.get(url)
   return res.text

@app.route('/getprice',methods=['GET'])
def getprice():
   chainid=request.args.get('chainid','1')
   url=ES_HOST+"?chainid="+chainid+"&module=stats&action=ethprice&apikey="+SK_ESTOKEN
   res=requests.get(url)
   return res.text

@app.route('/geturl',methods=['GET'])
def geturl():
   tourl=request.args.get('tourl')
   if not is_base64(tourl): return 'tourl error'
   url=str(base64.b64decode(tourl), 'utf-8')
   res=requests.get(url)
   return res.text

@app.route('/getcmcurl',methods=['GET'])
def getcmcurl():
   headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': SK_CMCKEY}
   tourl=request.args.get('tourl')
   if tourl=='':
      tourl='/v1/cryptocurrency/listings/latest'
   else:
      if not is_base64(tourl): return 'tourl error'
      tourl=str(base64.b64decode(tourl), 'utf-8')
      
   partxt=request.args.get('partxt')
   if partxt=='':
      parameters = {}
   else:
      if not is_base64(partxt): return 'partxt error'
      partxt=str(base64.b64decode(partxt), 'utf-8')
      parameters=json.loads(partxt)
      
   url = 'https://pro-api.coinmarketcap.com'+tourl
   
   #app.logger.info('tourl:%s', tourl)
   #app.logger.info('partxt:%s', partxt)
   app.logger.info('parameters:%s', parameters)
   app.logger.info('url:%s', url)
   
   session = requests.Session()
   session.headers.update(headers)
   res=session.get(url,params=parameters)
   #app.logger.info('res.text:%s', res.text)
   return res.text
   
@app.route('/getcac',methods=['GET'])
def getcac():
   host="red-ctipejggph6c738b3u90"
   r = redis.Redis(host, port=6379, db=0)
   r.set('mykey', 'myvalue')
   return r.get('mykey')
   
@app.route('/getexcrate',methods=['GET'])
def get_exchange_rate():
   curr=request.args.get('curr')
   if not is_base64(curr): return 'curr error'
   if curr!='':
       curr=str(base64.b64decode(curr), 'utf-8')
       curr=curr.upper()
   else:
       curr='USD'
   url = 'https://v6.exchangerate-api.com/v6/'+SK_EXCKEY+'/latest/'+curr
   res = requests.get(url)
   return res.text
   
@app.route('/getlist',methods=['GET'])   
def getlist():
   flestr="/etc/secrets/list.txt"
   i=0
   lrsp=""
   with open(flestr, 'r') as file:
       for line in file:
           i=i+1
           if(i>10):break
           addr=line.strip()
           lrsp=lrsp+'<br>'+addr
           print(addr)
   return lrsp
   
if __name__ == '__main__':
   SK_ESTOKEN= os.environ.get('SK_ESTOKEN')
   SK_CMCKEY= os.environ.get('SK_CMCKEY')
   SK_EXCKEY= os.environ.get('SK_EXCKEY')
   SK_PORT= os.environ.get('SK_PORT','82')
   app.run('0.0.0.0',SK_PORT,True)
