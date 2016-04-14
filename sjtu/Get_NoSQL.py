# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import fileinput
import urllib
import bs4
import re
from json import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def dict_add( dict_1, key, dict_2 ):
    if dict_1.has_key(key):
        if isinstance( dict_1[key], list):
            dict_1[key].append( dict_2 )
        else:
            dict_1[key] = [dict_1[key], dict_2]
    else:
        dict_1[key] = dict_2
    return dict_1

def dfs_dom_tree( node ):
    data = {}
    name = getattr(node, "name", None)
    if name is not None:
        dic = getattr(node, "attrs", None)
        for key in dic:
            node_att = unicode('@' + key).encode('utf-8')
            node_att_value = urllib.quote((unicode(dic[key])).encode('utf8'))
            data[node_att] = node_att_value

        for child in node.children:
            sub_list = dfs_dom_tree( child )
            data = dict_add( data, sub_list[0], sub_list[1] )

        return [name, data]

    elif isinstance(node, bs4.element.NavigableString) and ( not isinstance(node, bs4.element.Comment) ) :
        data = urllib.quote((unicode(node.string)).encode('utf8'))
        return ['#text', data]

zz_num = 0
filename = 'MongoDB_data.txt'
total_flag = 0

for line in fileinput.input("url.txt"):
    link = line.strip('\n')
    req = urllib2.Request(link)


#    print "ready"

    flag = 0
    while (flag >= 0):
        try:
            res = urllib2.urlopen(req)
        except Exception, e:
            flag = flag + 1
            total_flag = total_flag + 1
            print 'failed ' + str(flag) + ' times'
        else:
            flag = -1

    data = {}
    the_page = res.read()



#    print the_page
    the_page = re.sub('[\n \t\r]',' ', the_page)
    soup = BeautifulSoup(the_page,'lxml')

    sub_list = dfs_dom_tree( soup.html )
    data = dict_add( data, sub_list[0], sub_list[1] )
    data['url'] = link

#    print data['html']
#    input()

#    data = JSONEncoder().encode(data)
    data = unicode(data).encode('utf-8')

    with open(filename, 'a') as f:
        f.write(data)

    zz_num = zz_num + 1

    print 'done[ ' + str(zz_num) + ' ]: ' + link

print str(total_flag) + ' fails'
