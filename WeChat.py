import time
import requests
import json
import os

class WeChat:
    def __init__(self):
        self.CORPID = ''
        self.CORPSECRET = ''
        self.AGENTID = ''
        self.TOUSER = ""
		self.set_opt()

    def __call__(self): 
          return self
    
    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        #print(data)
        return data["access_token"]

    def set_opt(self,arg):
        self.CORPID=os.environ.get('SK_CORPID')
        self.CORPSECRET=os.environ.get('CORPSECRET')
        self.AGENTID=os.environ.get('AGENTID')
        self.TOUSER=os.environ.get('TOUSER')

    def get_access_token(self):
        try:
            with open('./tmp/access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('./tmp/access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('	'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('./tmp/access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('	'.join([str(cur_time), access_token]))
                    return access_token
 
    def send_data(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
                },
            "safe": "0"
            }
        send_msges=(bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]
 
 
if __name__ == '__main__':
    wx = WeChat()
    wx.send_data("test")
