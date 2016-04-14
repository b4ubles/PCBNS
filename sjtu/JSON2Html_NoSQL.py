import xmltodict
from json import *
import fileinput

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def checkout( dictVal ):
    for key in dictVal:
    #    print "hh"
        if ( ( key == "@src" ) or ( key == "@href" ) ):
    #        print key
    #        print dictVal[key]
            if (dictVal[key][0] == '/'):
                dictVal[key] = url_1 + dictVal[key]
            elif ( dictVal[key][0:3] != 'http' ):
                dictVal[key] = url_2 + dictVal[key]
        if isinstance( dictVal[key], dict ):
            checkout( dictVal[key] )
        if isinstance( dictVal[key], list ):
            for sub_dict in dictVal[key]:
                if isinstance( sub_dict, dict ):
                    checkout( sub_dict )

for line in fileinput.input("input_NoSQL.txt"):
    dictVal = JSONDecoder().decode(line)
    cutname = dictVal["url"].split('/')
    filename = cutname[-1]
    url_1 = cutname[0] + '//' + cutname[2]
    url_2 = dictVal["url"][:-len(cutname[-1])]
    del dictVal["url"]
    #print filename
    #print dictVal
#    print dictVal
    checkout(dictVal)

    data = xmltodict.unparse(dictVal, pretty = True)
    data.replace('gb2312','utf-8')
    #print data

    with open(filename, 'w') as f:
        f.write(data)
    #print data
    print 'done: ' + filename
