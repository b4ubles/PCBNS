import socket
import MySQLdb
import pprint
from urllib import unquote


def getChild(k):
    res = {}
    getchild = 'select * from {}.html where father={}'.format(DATABASE, k)
    if PRINT_SQL:
        print getchild
    of.write(getchild+';\n')
    cur.execute(getchild)
    childres = cur.fetchall()
    for record in childres:
        t = record[1]
        if t[0] in ('#',  '@'):
            getvalue = 'select value from {}.value where k={}'.format(DATABASE, record[3])
            if PRINT_SQL:
                print getvalue
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
    if PRINT_SQL:
        print geturl
    of.write(geturl+';\n')
    cur.execute(geturl)
    urlres = cur.fetchall()
    #print urlres
    urlkey = urlres[0][3]
    res['html'] = getChild(urlkey)
    res['url'] = url
    return res


s = socket.socket()

host = socket.gethostname()
port = 6674
s.bind((host,port))

s.listen(5)

PRINT_SQL = True
DATABASE = 'test'
of = open('out.sql', 'w+',1)
conn = MySQLdb.connect('localhost', 'root', '0277', 'test')
cur=conn.cursor()

while True:
	c,addr = s.accept()
	print 'Got connection from', addr
	c.close()
	break

s.close()

f = open('url')
for i in range(20):
    resd = sql2json('http://www.jwc.sjtu.edu.cn/web/sjtu/198097-1980000000391.htm')
#print resd
'''
num = 1
for url in open('url.txt'):
    sql2json(url.strip())
    print num               # num is used to show the process of the program.
    num += 1'''

f.close()
of.close()
conn.close()

import subprocess
p = subprocess.Popen(['mysqlslap','--create', 'use test', '--query', 'out.sql', '-uroot', '-p0277'])
