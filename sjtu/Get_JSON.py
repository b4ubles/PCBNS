import urllib2
from bs4 import BeautifulSoup
from json import *
import xmltodict
import fileinput

zz_num = 0;

for line in fileinput.input("url.txt"):
    req = urllib2.Request(line)
    res = urllib2.urlopen(req)
    the_page = res.read()
    soup = BeautifulSoup(the_page,'xml')
    doc = xmltodict.parse(soup.prettify())
    output = JSONEncoder().encode(doc)
    filename = 'MongoDB_data.json'
    data = output + '\n'
    with open(filename, 'a') as f:
        f.write(data)
    zz_num = zz_num + 1
    print 'done[ '+ str(zz_num) + ' ]: '  + line
