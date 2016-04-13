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

def dfs_dom_tree(node, formo):
    global key_rank
    global link
    global filename
    with open(filename, 'a') as f:
        f.write(formo + '\n')
    name = getattr(node, "name", None)
    if name is not None:
        key_rank = key_rank + 1
        num = str(key_rank)
        type_data = str(name)
        data_0 = type_data + '(' + num + ')'
        data = formo + '---' + data_0 + '\n'
        with open(filename, 'a') as f:
            f.write(data)

        new_formo = formo + '   ' + ' ' * (len(data_0) >> 1) + '|'
#        print new_formo


        dic = getattr(node, "attrs", None)
        for key in dic:
            key_rank = key_rank + 1
            with open(filename, 'a') as f:
                f.write(new_formo + '\n')
            type_data = '@' + key
            num = str(key_rank)
            data_0 = type_data + '(' + num + ')'
            data = new_formo + '---' + data_0 + '\n'
            with open(filename, 'a') as f:
                f.write(data)

        for child in node.children:
            dfs_dom_tree(child, new_formo)

    elif isinstance(node, bs4.element.NavigableString) and ( not isinstance(node, bs4.element.Comment) ) :
        key_rank = key_rank + 1
        num = str(key_rank)
        type_data = '#text'
        data_0 = type_data + '(' + num + ')'
        data = formo + '---' + data_0 + '\n'
        with open(filename, 'a') as f:
            f.write(data)

zz_num = 0
key_rank = 0;
total_flag = 0

for line in fileinput.input("Demo_url.txt"):
    link = line.strip('\n')
    filename = link.split('/')[-1]
    filename = filename.split('.')[0] + '.txt'
    data = line
    with open(filename, 'wr') as f:
        f.write(data)
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
    dfs_dom_tree(soup.html, '|')
    zz_num = zz_num + 1

    print 'done[ ' + str(zz_num) + ' ]: ' + link
    print 'Get_SQL.py has found ' + str(key_rank) + ' nodes'
    print ' '
    print ' '
    print ' '
    print 'Table_one SQL_data:'
    print '-----------------------------------------------------------------------------------------------------'
    print "|" + "Link".center(70) + "|" + "Type".center(10) + "|" + "father".center(8) + "|" + "Key".center(8) + "|"
    print '-----------------------------------------------------------------------------------------------------'
    print "|" + link.center(70) + "|" + "strong".center(10) + "|" + str(1231).center(8) + "|" + str(1234).center(8) + "|"
    print '-----------------------------------------------------------------------------------------------------'
    print ' '
    print ' '
    print ' '
    print ' '
    print 'Table_twl SQL_data_value:'
    print '-----------------------------------------------------------------------------------------------------'
    print "|" + "Key".center(10) + "|" + "Value".center(88) + "|"
    print '-----------------------------------------------------------------------------------------------------'
    print "|" + str(12324).center(10) + "|" + "It%20is%20an%20example.".center(88) + "|"
    print '-----------------------------------------------------------------------------------------------------'
    print ' '
    print ' '
    print ' '
    print ' '

print 'Get_SQL_Stru.py has occured ' + str(total_flag) + ' fails'
