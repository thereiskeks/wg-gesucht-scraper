import requests
from lxml.etree import _Attrib
from pyquery import PyQuery as pq
from collections import namedtuple
import sys

parameters = sys.argv

class Offer(object):
    pass

lastid=''
try:
    with open('lastid.tmp', 'r') as f:
        lastid = f.read().strip()
except:
    pass

def bot_sendtext(bot_message):
    ### Send text message
    print("sending")
    bot_token = parameters[1]
    bot_chatID = parameters[2]
    send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id=' + bot_chatID + '&text=' + bot_message
    print(send_text)
    requests.get(send_text)


resp = requests.get('https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.0.html#back_to_ad_3689803')
d = pq(resp.text)
trs:_Attrib = d('#main_column div.panel')
ids = [tr.attrib['data-id'] for tr in trs if tr.attrib.has_key("data-id")]
print("-")



try:
    lastpos = ids.index(lastid)
except:
    lastpos = len(ids)
if lastpos == 0:
    exit(1)
else:
    trs = trs[:lastpos]
    ids = ids[:lastpos]

def generateLink(id):
    return 'http://wg-gesucht.de/' + id + ".html"

data = [generateLink(e) for e in ids]
print('\n'.join('\t'.join(e) for e in data).encode('utf-8'))
open('lastid.tmp', 'w').write(ids[0])


import datetime
import time
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d %H:%M:%S')
bot_sendtext("I, your android of choice, found new Flats for you: \n\r"+st)

for link in data:
    bot_sendtext(link)




