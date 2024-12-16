from flask import Flask
import os

app = Flask(__name__)
SK_CORPID = os.getenv('SK_CORPID')
@app.route('/')
def hello_world():
   return 'Hello World'+SK_CORPID

if __name__ == '__main__':
   app.run('0.0.0.0',82,True)
