# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import fileinput
import urllib
import bs4
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def dfs_dom_tree(node, father_rank):
    global key_rank
    global link
    global filename
    name = getattr(node, "name", None)
    if name is not None:
        key_rank = key_rank + 1
        father = key_rank
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

        id_data = urllib.quote(id_data)
        class_data = urllib.quote(class_data)
        num1 = urllib.quote(str(father_rank))
        num2 = urllib.quote(str(key_rank))
        value_data = urllib.quote(value_data)
        type_data = urllib.quote(name)
        data = type_data + ',' + link + ',' + id_data + ',' + class_data + ',' + num1 + ',' + num2 + ',' + value_data + '\n'

        with open(filename, 'a') as f:
            f.write(data)

        print 'Get_SQL.py has made ' + str(key_rank) + ' nodes'
        #print data
        for child in node.children:
            dfs_dom_tree(child, father)

    elif isinstance(node, bs4.element.NavigableString) and unicode(node.string) != u"\n":
        key_rank = key_rank + 1
        value_data = unicode(node.string).encode('utf-8')
        id_data = urllib.quote('None')
        class_data = urllib.quote('None')
        num1 = urllib.quote(str(father_rank))
        num2 = urllib.quote(str(key_rank))
        value_data = urllib.quote(value_data)
        type_data = urllib.quote('text')
        data = type_data + ',' + link + ',' + id_data + ',' + class_data + ',' + num1 + ',' + num2 + ',' + value_data + '\n'

        with open(filename, 'a') as f:
            f.write(data)
        print 'Get_SQL.py has made ' + str(key_rank) + ' nodes'


zz_num = 0
key_rank = 0
total_flag = 0
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
            total_flag = total_flag + 1
            print 'failed ' + str(flag) + ' times'
        else:
            flag = -1

    the_page = res.read()
    the_page = re.sub('[\n \t\r]',' ', the_page)
    soup = BeautifulSoup(the_page,'lxml')
    link = urllib.quote(link)
    dfs_dom_tree(soup.html, 0)
    zz_num = zz_num + 1

    print 'done[ ' + str(zz_num) + ' ]: ' + link

print 'Get_SQL.py has occured ' + str(total_flag) + ' failures'
