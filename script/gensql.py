#!/usr/bin/python
'''
Mysql Version: 14.14 Distrib 5.6.28, for debian-linux-gnu (x86_64) using  EditLine wrapper

'''

import random
import os

UNIQUE_QUERY_NUM = 1000
TEST_DATABASE = 'test'
TEST_TABLE = 'test3'
READ_COLOMN = 'a'
INSERT_COLUMN = 'b'
UPDATE_COLUMN = 'c'
QUERY_FILE = '/tmp/answersql'
INSERT_RECORD_FILE = '/tmp/insertquery'
OUTFILE = 'out.sql'
TOTAL_NUM = 1000000

def genread(totalNum, uniqueNum = None):
    if uniqueNum == None:
        uniqueNum = totalNum
    if uniqueNum > UNIQUE_QUERY_NUM:
        raise Exception("Exceed the number of all records.")
    with open(QUERY_FILE, 'r') as f:
        answerSeq = f.read().split()
    randomAnswerSeq = random.sample(answerSeq, uniqueNum)
    for _ in xrange(totalNum):
        toquery = random.choice(randomAnswerSeq)
        yield 'select * from {}.{} where {}="{}";\n'.format(TEST_DATABASE, TEST_TABLE, READ_COLOMN, toquery)

def genwrite(totalNum):
    f = open(INSERT_RECORD_FILE, 'a')
    for _ in xrange(totalNum):
        toinsert = os.urandom(50).encode('hex')
        f.write(toinsert+'\n')
        yield 'insert into {}.{}({}) values ("{}");\n'.format(TEST_DATABASE, TEST_TABLE, INSERT_COLUMN, toinsert)
    f.close()

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
    tmp = []
    num = 10000 / eachNum
    for i in xrange(idNum):
        ID = 'user' + os.urandom(9).encode('hex')
        for __ in xrange(eachNum):
            tmp += ['("{}", "{}", "{}", "{}", "{}")'.\
                     format(ID, os.urandom(50).encode('hex'), os.urandom(50).encode('hex'), os.urandom(50).encode('hex'), os.urandom(50).encode('hex'))]
        if (i+1) % num == 0:
            yield 'insert into {}.{} values {};\n'.format(TEST_DATABASE, TEST_TABLE, ','.join(tmp))
            tmp = []

#CONFIG = {genread: 0.9, genwrite: 0.1}
#CONFIG = {genwrite: 1}
#CONFIG = {genupdate: 0.1, gendelete: 0.1}
CONFIG = {gencreate: 1}

if __name__ == '__main__':
    randbox = []
    for i in CONFIG:
        randbox += [i(int(CONFIG[i] * TOTAL_NUM))] * int(CONFIG[i] * TOTAL_NUM + 1)
    random.shuffle(randbox)
    fout = open(OUTFILE, 'w+')
    for gen in randbox:
        try:
            query = gen.next()
            fout.write(query)
        except StopIteration:
            pass
    fout.close()
