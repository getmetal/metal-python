import requests
from .typings import IndexPayload, SearchPayload, TunePayload

BASE_API = 'https://api.getmetal.io/v1'


class Metal:
  api_key: str
  client_id: str
  app_id: str

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
  
  def __getData(self, app, payload: dict = {}):
    data = { 'app': app }
    if (payload.get('imageBase64') is not None):
      data['imageBase64'] = payload['imageBase64']
    elif (payload.get('imageUrl') is not None):
      data['imageUrl'] = payload['imageUrl']
    elif (payload.get('text') is not None):
      data['text'] = payload['text']
    elif (payload.get('embedding') is not None):
      data['embedding'] = payload['embedding']
    
    return data
  
  def __validateIndexAndSearch(self, app = None, payload = {}):
    if (app is None):
        raise TypeError('app_id required')
    
    if (payload.get('imageBase64') is None and payload.get('imageUrl') is None and payload.get('text') is None and payload.get('embedding') is None):
      raise TypeError('imageBase64, imageUrl, text, or embedding required')
    

  def index(self, payload: IndexPayload = {}, app_id = None):
    headers = self.__get_headers()
    app = self.app_id or app_id
    self.__validateIndexAndSearch(app, payload)
    data = self.__getData(app, payload)
    r = requests.post(BASE_API + '/index', json=data, headers=headers)
    return r.json()
  
  def search(self, payload: SearchPayload = {}, app_id = None):
    headers = self.__get_headers()
    app = app_id or self.app_id
    self.__validateIndexAndSearch(app, payload)
    data = self.__getData(app, payload)

    r =  requests.post(BASE_API + '/search', json=data, headers=headers)
    return r.json()
  
  def tune(self, payload: TunePayload = {}, app_id = None):
    headers = self.__get_headers()
    app = app_id or self.app_id

    if (app is None):
        raise TypeError('app_id required')
    
    idA = payload.get('idA')
    idB = payload.get('idB')
    label = payload.get('label')
    if (idA is None or idB is None or label is None):
      raise TypeError('idA, idB, and label required')
  
    

    url = BASE_API + '/apps/' + app + '/tunings'
    data = { 'idA': idA, 'idB': idB, 'label': label }
    r =  requests.post(url, json=data, headers=headers)
    return r.json()
