import xmltodict
from json import *
from pymongo import MongoClient

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    conn = MongoClient('localhost')
    db = conn.html
    col = db.table
    dictVal = (col.find_one())
    #print dictVal

    #line = json.loads(l)
    #print line
    
    #dictVal = json.JSONDecoder().decode(l)
    print dictVal["url"]
    filename = dictVal["url"].split('/')[-1]
    del dictVal["url"]
    #print filename
    #print dictVal
    dictVal = {"root":dictVal}
    data = xmltodict.unparse(dictVal, pretty = True)
    #print data
    f =  open(filename, 'w')
    f.write(data)
    
