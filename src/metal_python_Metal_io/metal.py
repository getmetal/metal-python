import requests


BASE_API = 'https://api.getmetal.io/v1'


class Metal:
  def __init__(self, apiKey, clientId, appId):
    self.apiKey = apiKey
    self.clientId = clientId
    self.appId = appId
  
  def __getHeaders(self):
    return {
      'Content-Type': 'application/json',
      'x-metal-api-key': self.apiKey,
      'x-metal-client-id': self.clientId,
    }

  def index(self, payload = {}):
    headers = self.__getHeaders()
    data = { 'app': self.appId, }
    data.update(payload)

    r = requests.post(BASE_API + '/index', data=data, headers=headers)
    return r.json()
  
  def search(self, payload = {}):
    headers = self.__getHeaders()
    data = { 'app': self.appId, }
    data.update(payload)

    r =  requests.post(BASE_API + '/search', data=data, headers=headers)
    return r.json()
  
  def tune(self, payload = {}):
    headers = self.__getHeaders()
    data = { 'app': self.appId, }
    data.update(payload)

    r =  requests.post(BASE_API + '/tunings', data=data, headers=headers)
    return r.json()
