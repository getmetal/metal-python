import requests


BASE_API = 'https://api.getmetal.io/v1'


class Metal:
  def __init__(self, api_key, client_id, app_id = None):
    self.api_key = api_key
    self.client_id = client_id
    self.app_id = app_id
  
  def __get_headers(self):
    return {
      'Content-Type': 'application/json',
      'x-metal-api-key': self.api_key,
      'x-metal-client-id': self.client_id,
    }

  def index(self, payload = {}):
    headers = self.__get_headers()
    data = { 'app': self.app_id, }
    data.update(payload)

    r = requests.post(BASE_API + '/index', data=data, headers=headers)
    return r.json()
  
  def search(self, payload = {}):
    headers = self.__get_headers()
    data = { 'app': self.app_id, }
    data.update(payload)

    r =  requests.post(BASE_API + '/search', data=data, headers=headers)
    return r.json()
  
  def tune(self, payload = {}):
    headers = self.__get_headers()
    data = { 'app': self.app_id, }
    data.update(payload)

    r =  requests.post(BASE_API + '/tunings', data=data, headers=headers)
    return r.json()
