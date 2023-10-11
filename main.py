import requests
import json
from websockets.sync.client import connect
from names import names
import random
import time
import threading

game = input('Game ID: ')
number = input('Number of bots: ')
mon = input('Do you want the bots to get money, y/n: ')
nm = input('Do you want to use randomly generated names, y/n: ')
if nm == 'n':
  txtfil = input('Name of text file with names: ')

def run():
  session = requests.Session()
  cokk = session.get('https://play.blooket.com/play')
  
  headers = {
    "authority": "fb.blooket.com",
    "method": "GET",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json, text/plain, */*",
    "method": "PUT",
    "path": "/c/firebase/join",
    "scheme": "https",
    "Cookie": f"bsid={session.cookies.get_dict()['bsid']}; _b_csrf_id={session.cookies.get_dict()['_b_csrf_id']}",
    "Dnt": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
  }
  
  headers1 = {
    "authority": "identitytoolkit.googleapis.com",
    "method": "GET",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json, text/plain, */*",
    "method": "PUT",
    "path": "/v1/accounts:signInWithCustomToken?key=AIzaSyCA-cTOnX19f6LFnDVVsHXya3k6ByP_MnU",
    "scheme": "https",
    "X-Firebase-Gmpid": "1:741533559105:web:b8cbb10e6123f2913519c0",
    "Dnt": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
  }
  
  name = random.choice(names)
  data = {"id":f"{game}","name":name}
  print(data)
  
  response = requests.put('https://fb.blooket.com/c/firebase/join', headers=headers, json=data).text
  
  tok = json.loads(response)['fbToken']
  dat = {"token": tok, "returnSecureToken": 'true'}
  
  resp = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key=AIzaSyCA-cTOnX19f6LFnDVVsHXya3k6ByP_MnU', headers=headers1, json=dat).text
  
  idTok = json.loads(resp)['idToken']
  refresh = json.loads(resp)['refreshToken']
  second = {"t":"d","d":{"r":5,"a":"p","b":{"p":f"/{game}/c/{name}","d":{"b":"Dragon"}}}}	
  
  web = connect(f"{json.loads(response)['fbShardURL'].replace('https', 'wss')}.ws?v=5&p=1:741533559105:web:b8cbb10e6123f2913519c0")
  web.send('{"t":"d","d":{"r":1,"a":"s","b":{"c":{"sdk.js.9-23-0":1}}}}')
  
  jzo = {"t":"d","d":{"r":2,"a":"auth","b":{"cred":f"{idTok}"}}}
  web.send(json.dumps(jzo))
  jzo1 = {"t":"d","d":{"r":3,"a":"q","b":{"p":f"/{game}","h":""}}}
  web.send(json.dumps(jzo1))
  jzo2 = {"t":"d","d":{"r":4,"a":"n","b":{"p":f"/{game}"}}}
  web.send(json.dumps(jzo2))
  web.send(json.dumps(second))
  jzo3 = {"t":"d","d":{"r":6,"a":"q","b":{"p":f"/{game}/c","h":""}}}
  web.send(json.dumps(jzo3))
  jzo4 = {"t":"d","d":{"r":7,"a":"q","b":{"p":f"/{game}/stg","h":""}}}
  web.send(json.dumps(jzo4))
  gold = random.randint(5,100)
  count = 8
  while True:
    if mon == 'y':
      time.sleep(random.randint(5,20))
      jzo5 = {"t":"d","d":{"r":count,"a":"p","b":{"p":f"/{game}/c/{name}","d":{"b":"Dragon","g":gold}}}}	
      web.send(json.dumps(jzo5))
      gold = round(gold ** (1 + (random.randint(1,5)/100)))
      count = count + 1
    else:
      time.sleep(15)
      web.send('0')

for x in range(int(number)):
  time.sleep(0.25)
  threading.Thread(target=run).start()
