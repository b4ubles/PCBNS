import xmltodict
import ast
import fileinput
import urllib
from json import *
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def zz_decode( url_str ):
    return urllib.unquote( url_str )

def JSON2Html( key, zz_type ):
    global url_1
    global url_2
    if isinstance(zz_type, dict):
        tag_name = key
        tag_page = ''
        for sub_key in zz_type:
            if (sub_key[0] == '@'):
                zz_content = ''
                if (sub_key == '@content' ):
                    zz_content = 'text/html; charset=utf-8'
                else:
                    zz_content = zz_decode(zz_type[sub_key])
                zz_content = zz_content.replace("'","")
                zz_content = zz_content.replace("[","")
                zz_content = zz_content.replace("]","")
                zz_content = zz_content.replace(","," ")
                if ((sub_key == '@src' or sub_key == '@href') and (zz_content != "")):
                    if ( zz_content[0] == '/' ):
                        zz_content = url_1 + zz_content
                    elif ( zz_content[:3] != 'http' ):
                        zz_content = url_2 + zz_content
                tag_name = tag_name + ' '
                tag_name = tag_name + sub_key[1:] + '="'
                tag_name = tag_name + zz_content + '"'
            else:
                tag_page = tag_page + JSON2Html( sub_key, zz_type[sub_key] )
        outp = ' <' + tag_name + '> ' + tag_page + ' </' + key + '> '
        return outp
    if isinstance(zz_type, list):
        page = ''
        for sub_page in zz_type:
            page = page + JSON2Html( key, sub_page )
        return page
    return zz_decode( zz_type )

if __name__ == '__main__':

    trans_flag = sys.argv[1]
    if (trans_flag == 'S'):
        input_file = 'MySQL_data.txt'
    elif (trans_flag == 'N'):
        input_file = 'MongoDB_data.txt'
    else:
        print 'Error: Wrong arguements.'
        print "ONLY 'S' and 'N' are allowed"
        exit()

    for line in fileinput.input(input_file):
        dictVal = ast.literal_eval(line)
#        dictVal = eval(line)
#        print dictVal["url"]
#        input()
#        dictVal = JSONDecoder().decode(line)
        cutname = dictVal["url"].split('/')
        filename = cutname[-1]
        if (filename[-3:] != "htm"):
            filename = filename + '.htm'
        filename = trans_flag + '_' + filename
        url_1 = cutname[0] + '//' + cutname[2]
        url_2 = dictVal["url"][:-len(cutname[-1])]
        if (dictVal['url'] == "http://electsys.sjtu.edu.cn"):
            url_2 = "http://electsys.sjtu.edu.cn/"
        del dictVal["url"]

        tag_name = 'html'
        the_page = JSON2Html( "head", dictVal['html']['head'])
        the_page = the_page + JSON2Html( "body", dictVal['html']['body'])
        for sub_key in dictVal['html']:
            if (sub_key[0] == '@'):
                tag_name = tag_name + ' '
                tag_name = tag_name + sub_key[1:] + '="'
                tag_name = tag_name + zz_decode(dictVal['html'][sub_key]) + '"'

        data = ' <' + tag_name + '> ' + the_page + ' </html> '
        data = data.encode('utf-8')

        with open(filename, 'w') as f:
            f.write(data)

        print 'done: ' + filename
