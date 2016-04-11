import xmltodict
from json import *
import fileinput

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

for line in fileinput.input("MongoDB_data.json"):
    dictVal = JSONDecoder().decode(line)
    filename = dictVal["url"].split('/')[-1]
    del dictVal["url"]
    #print filename
    #print dictVal
    data = xmltodict.unparse(dictVal, pretty = True)
    #print data

    with open(filename, 'w') as f:
        f.write(data)
    #print data
    print 'done: ' + filename
