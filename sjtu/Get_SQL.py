# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import fileinput
import urllib
import bs4

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
        key_rank = key_rank + 1
        dic = getattr(node, "attrs", None)

        if dic.has_key('id'):
            id_data = unicode(dic['id']).encode('utf-8')
        else:
            id_data = 'None'

        if dic.has_key('class'):
            class_data = unicode(dic['class']).encode('utf-8')
        else:
            class_data = 'None'

        value_data = 'None'

        id_data = urllib.quote_plus(id_data)
        class_data = urllib.quote_plus(class_data)
        num1 = urllib.quote_plus(str(father_rank))
        num2 = urllib.quote_plus(str(key_rank))
        value_data = urllib.quote_plus(value_data)
        type_data = urllib.quote_plus(name)
        data = type_data + ',' + link + ',' + id_data + ',' + class_data + ',' + num1 + ',' + num2 + ',' + value_data + '\n'

        with open(filename, 'a') as f:
            f.write(data)

        print 'Get_SQL.py has made ' + str(key_rank) + ' nodes'
        #print data
        for child in node.children:
            dfs_dom_tree(child, father)

    elif isinstance(node, bs4.element.NavigableString):
        key_rank = key_rank + 1
        value_data = unicode(node.string).encode('utf-8')
        id_data = urllib.quote_plus('None')
        class_data = urllib.quote_plus('None')
        num1 = urllib.quote_plus(str(father_rank))
        num2 = urllib.quote_plus(str(key_rank))
        value_data = urllib.quote_plus(value_data)
        type_data = urllib.quote_plus('text')
        data = type_data + ',' + link + ',' + id_data + ',' + class_data + ',' + num1 + ',' + num2 + ',' + value_data + '\n'

        with open(filename, 'a') as f:
            f.write(data)
        print 'Get_SQL.py has made ' + str(key_rank) + ' nodes'


zz_num = 0
key_rank = 0;
filename = 'SQL_data.txt'
data = 'tpye,url,id,class,father,key,value' + '\n'
with open(filename, 'a') as f:
    f.write(data)

for line in fileinput.input("url.txt"):
    link = line.strip('\n')
    req = urllib2.Request(link)

    flag = 0
    while (flag >= 0):
        try:
            res = urllib2.urlopen(req)
        except Exception, e:
            flag = flag + 1
            print 'failed ' + str(flag) + ' times'
        else:
            flag = -1

    the_page = res.read()
    soup = BeautifulSoup(the_page,'lxml')
    link = urllib.quote_plus(link)
    dfs_dom_tree(soup.html, 0)
    zz_num = zz_num + 1

    print 'done[ ' + str(zz_num) + ' ]: ' + link
