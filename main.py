import json
import requests
from datetime import datetime
from pprint import pprint


def cripto_migliore(data):
  best = data['data'][0]
  for val in data['data']:
    if (val['quote']['USD']['volume_24h'] > best['quote']['USD']['volume_24h']):
      best = val
  return {'name':best['name'],'volume':best['quote']['USD']['volume_24h']}
  
def sort_perc(data):
  new = sorted(data['data'], key= lambda k: k['quote']['USD']['percent_change_24h'],reverse=True )
  return new

def sort_cap(data):
  new = sorted(data['data'], key= lambda k: k['quote']['USD']['market_cap'],reverse=True )
  return new

def dict_create(data):
  risultato = {'data':{}}
  
  top_10 = {}
  worst_10 = {}
  top_20 = {}
  price_top_76 = {}
  perc_top_20 = {}


  top = sort_perc(data)
  for i in range(0,10):
    top_10[i+1] = {'name':top[i]['name'],'percentage':f'{top[i]["quote"]["USD"]["percent_change_24h"]}%'}

  j = 1
  for i in range((len(top)-1),(len(top)-11), -1):
    worst_10[j] = {'name':top[i]['name'],'percentage':top[i]['quote']['USD']['percent_change_24h']}
    j += 1

  top = sort_cap(data)

  for i in range(0,20):
    top_20[i+1] = {'name':top[i]['name'],'price':f'{top[i]["quote"]["USD"]["price"]}$'}

  j = 1
  for i  in range(0,len(top)):
    if (int(top[j]['quote']['USD']['volume_24h']) > int(76000000)):
      price_top_76[j] = {'name':top[i]['name'],'price':f'{top[i]["quote"]["USD"]["price"]}$'} 
      j += 1

  for i in range(0,19):
    perc_top_20[i] = {'name':top[i]['name'],'percentage':f'{top[i]["quote"]["USD"]["percent_change_24h"]}%'}

  risultato['data']['top_1'] = cripto_migliore(data)
  risultato['data']['top_10'] = top_10
  risultato['data']['worst_10'] = worst_10
  risultato['data']['price_top_20'] = top_20
  risultato['data']['price_top_76'] = price_top_76
  risultato['data']['perc_top_20'] = perc_top_20
  return risultato


# Generazione File 
current = datetime.now()
stringa = str(f'{current.day}-{current.month}-{current.year}.json')

url= 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'


parameters = {
  'start':'1',
  'limit':'100',
  'convert':'USD'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'INSERT_YOUR_KEY_HERE'
}



data = requests.get(url=url,headers=headers,params=parameters).json()


json_object = json.dumps(dict_create(data), indent = 4) 
with open(stringa, "w") as outfile: 
    outfile.write(json_object) 
