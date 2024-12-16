from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
   SK_CORPID = os.environ.get('SK_CORPID')
   return 'Hello World'+SK_CORPID

if __name__ == '__main__':
   app.run('0.0.0.0',82,True)
