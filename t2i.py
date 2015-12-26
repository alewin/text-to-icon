import urllib, urllib2
import json
import nltk
from nltk.tag import pos_tag
import gzip
from StringIO import StringIO


def get_icon(name):
    args = urllib.urlencode({'q': name, 'page': 1, 'limit': 1,'raw_html':'false'})
    url = "http://thenounproject.com/search/json/icon/?" + args
    
    req = urllib2.Request(url)
    req.add_header('Accept-Encoding', 'gzip, deflate, sdch')
    req.add_header('Connection', 'keep-alive')
    req.add_header('Host', 'thenounproject.com')
    req.add_header('Referer', 'https://thenounproject.com/search/?q='+name)
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
    
    
    try:
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = json.loads(f.read())
            return data["icons"][0]["icon_url"]
    except: 
        return ""

def text2icon(text,tags):
    index = 0
    progress = 0
    ws_ts = pos_tag(text.split())
    for word,tag in ws_ts:
        print '%d of %d' % (progress, len(ws_ts))
        if any(x in tag for x in tags):
            index = text.find(word,index,len(text))
            icon = get_icon(word)
            text = text[:index+len(word)] + " <img width='20' src ='" +icon +"'></img> " + text[index+len(word):]
        i += 1
    return text

print("Start")

fin = open("input.txt","r")
text = fin.read()
fin.close()

tags = ['NN'] #tags = ['NN,'VBP','JJ']
result = text2icon(text,tags)

fout = open("output.txt","w")
fout.write("<a>"+result+"</a>")
fout.close()

print("End")
