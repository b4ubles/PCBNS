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
    global filename_1
    name = getattr(node, "name", None)
    if name is not None:
        key_rank = key_rank + 1
        father = key_rank
        num1 = urllib.quote(str(father_rank))
        num2 = urllib.quote(str(key_rank))
        type_data = urllib.quote(name)
        data = link + ',' + type_data + ',' + num1 + ',' + num2 + '\n'
        with open(filename, 'a') as f:
            f.write(data)

        dic = getattr(node, "attrs", None)
        for key in dic:
            key_rank = key_rank + 1
            type_data = urllib.quote(unicode('@' + key).encode('utf-8'))
            value_data = urllib.quote((unicode(dic[key])).encode('utf-8'))
            num1 = urllib.quote(str(father))
            num2 = urllib.quote(str(key_rank))
            data_1 = link + ',' + type_data + ',' + num1 + ',' + num2 + '\n'
            data_2 = num2 + ',' + value_data + '\n'
            with open(filename, 'a') as f:
                f.write(data_1)
            with open(filename_1, 'a') as f:
                f.write(data_2)

        for child in node.children:
            dfs_dom_tree(child, father)

    elif isinstance(node, bs4.element.NavigableString) and ( not isinstance(node, bs4.element.Comment) ) :
        key_rank = key_rank + 1
        value_data = urllib.quote((unicode(node.string)).encode('utf-8'))
        num1 = urllib.quote(str(father_rank))
        num2 = urllib.quote(str(key_rank))
        type_data = urllib.quote('#text')

        data_1 = link + ',' + type_data + ',' + num1 + ',' + num2 + '\n'
        data_2 = num2 + ',' + value_data + '\n'
        with open(filename, 'a') as f:
            f.write(data_1)
        with open(filename_1, 'a') as f:
            f.write(data_2)

zz_num = 0
key_rank = 0;
filename = 'SQL_data.txt'
filename_1 = 'SQL_data_value.txt'
total_flag = 0

data = 'link,type,father,key' + '\n'
with open(filename, 'a') as f:
    f.write(data)

data = 'key,value' + '\n'
with open(filename_1, 'a') as f:
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
    print 'Get_SQL.py has found ' + str(key_rank) + ' nodes'

print str(total_flag) + ' fails'
