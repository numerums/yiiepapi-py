import requests
import hmac
import hashlib
import random
import string
import time
import urllib
import sys

class ApiClient(object):
    protocole = 'https'
    host = 'www.yiiep.com'
    port = '443'
    path = '/webapi/v1/'

    def __init__(self, testmode, publicKey, privateKey):
        self.testmode = testmode
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.baseUrl = self.protocole + "://" + self.host + ":" + self.port + self.path
        self.lastReply = ['']

    def getHash(self, data, key):
        if (sys.version_info > (3, 0)):
            return hmac.new(bytes(key, 'UTF-8'), bytes(data, 'UTF-8'), hashlib.sha256).hexdigest()
        else:
            return hmac.new(key, data, hashlib.sha256).hexdigest()

    def random_str(self, length = 16):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

    def getOrderedQS(self, params = None, rawencode = True):
        if(params is None):
            params = {}
        paramstr = []
        keys = list(params)
        keys.sort()
        for i in range(len(keys)):
            key = keys[i]
            if rawencode == True:
                paramstr.append("{}={}".format(urllib.quote(key, safe = ''), urllib.quote(params[key], safe = '')))
            else:
                paramstr.append("{}={}".format(key, params[key]))
            
        return '&'.join(paramstr)

    def sign(self, method, ressource, params):
        if self.testmode == True :
            params["mode"] = "test"
        else:
            params["mode"] = "real"
        
        params["time"] = int(round(time.time() * 1000))
        params['rseed'] = self.random_str()
        params['identity'] = self.publicKey

        request = []
        #Request Method
        request.append(method)
        #--Host
        request.append("{}:{}".format(self.host, self.port))
        #--Path
        request.append("{}{}".format(self.path, ressource))
        #--Query string - Sort before hashing
        request.append(self.getOrderedQS(params, False))
        toSign = "\n".join(request)
        #print(toSign)
        params['signature'] = self.getHash(toSign, self.privateKey)

        return params

    def query(self, ressource, params):
        #Signing
        signed = self.sign('GET', ressource, params)
        url = "{}{}?{}".format(self.baseUrl, ressource, self.getOrderedQS(signed, True))
        #print (url);
        try:
            response = requests.get(url, headers = {'content-type': 'application/json', 'Accept': 'application/json'});
            return self.parseResponse(response)
        except requests.RequestException as e:
            return {"success" : False, "message" : "Request Error - " + e.strerror, "status" : 0}

    def send(self, ressource, params):
        #Signing
        signed = self.sign('POST', ressource, params)
        url = "{}{}".format(self.baseUrl, ressource)
        #print (url)
        try:
            response = requests.post(url, data = signed, headers = {'Accept': 'application/json'})
            return self.parseResponse(response)
        except requests.RequestException as e:
            return {"success" : False, "message" : "Request Error - " + e.strerror, "status" : 0}

    def parseResponse(self, response):
        if (response.status_code == 200):
            return response.json()
        else:
            return {"success" : False, "message" : "Request Fail", "status" : response.status_code}

    def isSuccess(self, response):
        self.lastReply = response
        return ('success' in self.lastReply and self.lastReply['success'] == True )

    def data(self):
        return self.lastReply.get('data', None)

    def message(self):
        return self.lastReply.get('message', None)
        



    