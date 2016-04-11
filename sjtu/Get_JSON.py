import urllib2
from bs4 import BeautifulSoup
from json import *
import xmltodict
import fileinput
import chardet

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
zz_num = 0
error_num = 0

for line in fileinput.input("url.txt"):
    line = line.strip('\n')
    print 'Ready: ' + line
    req = urllib2.Request(line)
    res = urllib2.urlopen(req)
    the_page = res.read()
    chardet1 = chardet.detect(the_page)
    try:
        the_page = the_page.decode(chardet1['encoding']).encode('utf-8')
    except UnicodeDecodeError, e:
        error_num = error_num + 1
        print 'Error ' + str(error_num) + ' : ' + line
        filename = 'Error_url.txt'
        with open(filename, 'a') as f:
            f.write(line + '\n')
    else:
        pass
    #print the_page
    soup = BeautifulSoup(the_page,'xml')
    doc = xmltodict.parse(soup.prettify())
    doc['url'] = line
    output = JSONEncoder().encode(doc)
    filename = 'MongoDB_data.json'
    data = output + '\n'
    with open(filename, 'a') as f:
        f.write(data)
    zz_num = zz_num + 1
    print 'Done[ '+ str(zz_num) + ' ]: '  + line

print str(error_num) + ' fails'
