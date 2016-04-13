# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @author Lyle
# @version 2016-03-26

from flask import Flask
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for, abort, render_template, flash
from pymongo import MongoClient

import xmltodict
from json import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

DEBUG = True
SECRET_KEY = "prentend I'm a secret key,hhh"
app = Flask(__name__)
app.config.from_object(__name__)

#@app.route('/', methods = ['GET', 'POST'])
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
  if request.method == "POST":
    urlist = request.form["url"]
    genfile(urlist)
    url = urlist.split("/")[-1]
    return render_template(url)
  else:
    return "No such url in DB"

@app.route('/test')
def t():
  try:
    ret = []
    return render_template('index.html',ret = ret)
  except:
    return render_template('search.html')

def genfile(url):
	conn = MongoClient('localhost')
	db = conn.html
	col = db.table
	dictVal = (col.find_one({"url":url}))
	#print dictVal

	#line = json.loads(l)
	#print line

	#dictVal = json.JSONDecoder().decode(l)
	print dictVal["url"]
	filename = dictVal["url"].split('/')[-1]
	del dictVal["url"]
	#print filename
	#print dictVal
	dictVal = {"root":dictVal}
	data = xmltodict.unparse(dictVal, pretty = True)
	#print data
	f =  open("templates/"+filename, 'w')
	f.write(data)

if __name__ == "__main__":
	app.run('0.0.0.0',4576)
