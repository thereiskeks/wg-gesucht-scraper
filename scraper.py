import pickle

import requests
from lxml.etree import _Attrib
from pyquery import PyQuery as pq
from collections import namedtuple
import sys

parameters = sys.argv

class Offer(object):
    pass

lastid=''


def save_obj(obj, name ):
    with open( name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open( name + '.pkl', 'rb') as f:
        return pickle.load(f)

try:
    lastIds = load_obj("lastIds")
except:
    lastIds = {}

try:
    with open('lastid.tmp', 'r') as f:
        lastid = f.read().strip()


except:
    pass

def bot_sendtext(bot_message):
    ### Send text message
    if len(parameters) < 3:
        print("you need to povide a bot_token and a chat_id")
        return
    print("sending")
    bot_token = parameters[1]
    bot_chatID = parameters[2]
    send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id=' + bot_chatID + '&text=' + bot_message
    print(send_text)
    requests.get(send_text)


resp = requests.get('https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.0.html?csrf_token=12ab2271e0f9bbb7af82a6924b4d9022f0e43c8f&offer_filter=1&noDeact=1&city_id=90&category=0&rent_type=0&dFr=1551308400&dTo=1553986800')
d = pq(resp.text)
trs:_Attrib = d('#main_column div.panel')
ids = [tr.attrib['data-id'] for tr in trs if tr.attrib.has_key("data-id")]
print("-")



try:
    lastpos = ids.index(lastid)
except:
    lastpos = len(ids)


for id in ids:
    if id in lastIds:
        lastIds[id] += 1
    else:
        lastIds[id] = 0

if lastpos == 0:
    exit(1)
else:
    ids = ids[:lastpos]


def generateLink(id):
    return 'http://wg-gesucht.de/' + id + ".html"

data = [generateLink(e) for e in ids if lastIds[id] < 5]
print('\n'.join('\t'.join(e) for e in data).encode('utf-8'))
open('lastid.tmp', 'w').write(ids[0])

save_obj(lastIds, "lastIds")

import datetime
import time
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d %H:%M:%S')
bot_sendtext("I, your android of choice, found new Flats for you: \n\r"+st)

for link in data:
    bot_sendtext(link)




