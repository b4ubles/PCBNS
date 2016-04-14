import xmltodict
import ast
import fileinput
import urllib
import chardet

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def SQL2html( key, zz_type ):
    if isinstance(zz_type, dict):
        tag_name = key
        tag_page = ''
        for sub_key in zz_type:
            if (sub_key[0] == '@'):
                if (sub_key == '@content' ):
                    zz_type[sub_key] = urllib.quote('text/html; charset=utf-8')
                tag_name = tag_name + ' '
                tag_name = tag_name + sub_key[1:] + '="'
                tag_name = tag_name + urllib.unquote(zz_type[sub_key]) + '"'
            else:
#                tag_page = tag_page + SQL2html( sub_key, zz_type[sub_key] )
                tag_page = tag_page + SQL2html( sub_key, zz_type[sub_key] )
        outp = ' <' + tag_name + '> ' + tag_page + ' </' + key + '> '
        return outp
    if isinstance(zz_type, list):
        page = ''
        for sub_page in zz_type:
            page = page + SQL2html( key, sub_page )
        return page
    return urllib.unquote(zz_type)


for line in fileinput.input("test.txt"):
#    print line
    dictVal = ast.literal_eval(line)
#    print dictVal['html']['@xmlns']
#    print type(dictVal['html']['@xmlns'])
#    html_page = ""
#    filename = dictVal["url"].split('/')[-1]
#    del dictVal["url"]
    #print filename
    #print dictVal
    tag_name = 'html'
    the_page = SQL2html( "head", dictVal['html']['head'])
    the_page = the_page + SQL2html( "body", dictVal['html']['body'])
    for sub_key in dictVal['html']:
        if (sub_key[0] == '@'):
            tag_name = tag_name + ' '
            tag_name = tag_name + sub_key[1:] + '="'
            tag_name = tag_name + urllib.unquote(dictVal['html'][sub_key]) + '"'
    data = ' <' + tag_name + '> ' + the_page + ' </html> '
    #print data

    filename = "test.html"

    chardet1 = chardet.detect(data)
    data = data.encode('utf-8')

    with open(filename, 'w') as f:
        f.write(data)
    #print data
    print 'done: ' + filename
