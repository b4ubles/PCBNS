#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import pprint
from urllib import unquote

DATABASE = 'test'
of = open('out.sql', 'w+',1)
with open('mysql_passwd') as f:
    passwd = f.read().strip()
conn = MySQLdb.connect('localhost', 'root', passwd, 'test')
cur=conn.cursor()

def getChild(k):
    res = {}
    getchild = 'select * from {}.html where father={}'.format(DATABASE, k)
    of.write(getchild+';\n')
    cur.execute(getchild)
    childres = cur.fetchall()
    for record in childres:
        t = record[1]
        if t[0] in ('#',  '@'):
            getvalue = 'select value from {}.value where k={}'.format(DATABASE, record[3])
            of.write(getvalue+';\n')
            cur.execute(getvalue)
            try:
                tmp = cur.fetchone()[0]
            except TypeError as e:
                print getvalue,record
                raise e
        else:
            tmp = {}
            child = getChild(record[3])
            if child : tmp.update(child)
        if res.has_key(t):
            try:
                res[t] += [tmp]
            except TypeError:
                res[t] = [res[t], tmp]
        else:
            res[t] = tmp

        del tmp
    #print res,k
    return res

def sql2json(url):
    res = {}
    geturl = 'select * from {}.html where url="{}" and type="html"'.format(DATABASE, url)
    of.write(geturl+';\n')
    cur.execute(geturl)
    urlres = cur.fetchall()
    #print urlres
    urlkey = urlres[0][3]
    res['html'] = getChild(urlkey)
    return res

if __name__ == '__main__':
    #resd = sql2json('http://www.jwc.sjtu.edu.cn/web/sjtu/198097-1980000000391.htm')
    #pprint.pprint(resd)
    num = 1
    for url in open('url.txt'):
        sql2json(url.strip())
        print num               # num is used to show the process of the program.
        num += 1

f.close()
conn.close()
