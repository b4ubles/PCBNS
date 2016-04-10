# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import fileinput

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def dfs_dom_tree(node, father_rank):
    global key_rank
    global link
    global filename
    father = key_rank
    name = getattr(node, "name", None)
    if name is not None:
        dic = getattr(node, "attrs", None)

        if dic.has_key('id'):
            id_data = unicode(dic['id']).encode('utf-8')
        else:
            id_data = 'None'

        if dic.has_key('class'):
            class_data = unicode(dic['class']).encode('utf-8')
        else:
            class_data = 'None'

        if node.string:
            value_data = unicode(node.string).encode('utf-8')
        else:
            value_data = 'None'

        data = name + '\t' + link + '\t' + id_data + '\t' + class_data + '\t' + str(key_rank) + '\t' + str(father_rank) + '\t' + value_data + '\n'

        with open(filename, 'a') as f:
            f.write(data)

        #print data

        for child in node.children:
            key_rank = key_rank + 1
            dfs_dom_tree(child, father)

zz_num = 0
filename = 'SQL_data.txt'
data = 'tpye    url id  class  father  key  value' + '\n'
with open(filename, 'a') as f:
    f.write(data)

for line in fileinput.input("url.txt"):
    key_rank = 0;
    link = line.strip('\n')
    req = urllib2.Request(link)
    res = urllib2.urlopen(req)
    the_page = res.read()
    soup = BeautifulSoup(the_page,'lxml')
    dfs_dom_tree(soup.html, 0)
    zz_num = zz_num + 1

    print 'done[ ' + str(zz_num) + ' ]: ' + link
