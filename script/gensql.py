#!/usr/bin/python2.7
'''
Mysql Version: 14.14 Distrib 5.6.28, for debian-linux-gnu (x86_64) using  EditLine wrapper

'''

import random
import os

TEST_DATABASE = 'test'
TEST_TABLE = 'test1'
INSERT_COLUMN = 'id'
UPDATE_COLUMN = 'c'
INSERT_RECORD_FILE = '/tmp/4insertquery'
OUTFILE = '43.sql'
TOTAL_NUM = 10000

def genread(totalNum):
    with open(INSERT_RECORD_FILE, 'r') as f:
        answerSeq = f.read().split()
    for _ in xrange(totalNum):
        toquery = random.choice(answerSeq)
        yield 'select * from {}.{} where {}="{}";\n'.format(TEST_DATABASE, TEST_TABLE, INSERT_COLUMN, toquery)

def genwrite(totalNum):
    for _ in xrange(totalNum):
        toinsert = os.urandom(50).encode('hex')
        yield 'insert into {}.{}({}) values ("{}");\n'.format(TEST_DATABASE, TEST_TABLE, INSERT_COLUMN, toinsert)

def gendelete(totalNum):
    with open(INSERT_RECORD_FILE, 'r') as f:
        deleteSeq = f.read().split()
    if totalNum > len(deleteSeq):
        raise Exception("You can't delete so many records.")
    for _ in xrange(totalNum):
        todelete = deleteSeq.pop(random.randint(0, len(deleteSeq)-1))
        yield 'delete from {}.{} where {}="{}";\n'.format(TEST_DATABASE, TEST_TABLE, INSERT_COLUMN, todelete)
    with open(INSERT_RECORD_FILE, 'w') as f:
        f.writelines([i+'\n' for i in deleteSeq])

def genupdate(totalNum):
    with open(INSERT_RECORD_FILE, 'r') as f:
        querySeq = f.read().split()
    for _ in xrange(totalNum):
        toquery = random.choice(querySeq)
        toupdate = os.urandom(50).encode('hex')
        yield 'update {}.{} set {}="{}" where {}="{}";\n'.format(TEST_DATABASE, TEST_TABLE, UPDATE_COLUMN, toupdate, INSERT_COLUMN, toquery)

def gencreate(idNum, eachNum=1):
    f = open(INSERT_RECORD_FILE, 'w')
    tmp = []
    num = 1 / eachNum
    for i in xrange(idNum):
        ID = 'user' + os.urandom(9).encode('hex')
        f.write(ID+'\n')
        for __ in xrange(eachNum):
            tmp += ['("{}", "{}", "{}", "{}", "{}")'.\
                     format(ID, os.urandom(50).encode('hex'), os.urandom(50).encode('hex'), os.urandom(50).encode('hex'), os.urandom(50).encode('hex'))]
        if (i+1) % num == 0:
            yield 'insert into {}.{} values {};\n'.format(TEST_DATABASE, TEST_TABLE, ','.join(tmp))
            tmp = []

#CONFIG = {gencreate: 1}
#CONFIG = {genread: 0.1, genupdate: 0.9}
CONFIG = {genread: 0.6,genupdate: 0.1,genwrite: 0.3}
#CONFIG = {genread: 0.9,genupdate: 0.1}
#CONFIG = {genread: 1}


if __name__ == '__main__':
    randbox = []
    for i in CONFIG:
        randbox += [i(int(CONFIG[i] * TOTAL_NUM))] * int(CONFIG[i] * TOTAL_NUM + 1)
    random.shuffle(randbox)
    #print randbox
    fout = open(OUTFILE, 'w+')
    for gen in randbox:
        try:
            query = gen.next()
            fout.write(query)
        except StopIteration:
            pass
    fout.close()
