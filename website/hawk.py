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
import urllib

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
      url = "N_"+url
      return render_template(url)
    else:
      return "No such url in DB"

def zz_decode( url_str ):
	try:
		return urllib.unquote( url_str )
	except:
		return ''

def JSON2Html( key, zz_type ):
    global url_1
    global url_2
    if isinstance(zz_type, dict):
        tag_name = key
        tag_page = ''
        if zz_type.has_key( 'script' ):
            tag_page = tag_page + JSON2Html( 'script', zz_type['script'] )
        for sub_key in zz_type:
            if (sub_key != 'script'):
                if (sub_key[0] == '@'):
                    zz_content = ''
                    if (sub_key == '@content' ):
                        zz_content = 'text/html; charset=utf-8'
                    else:
                        zz_content = zz_decode(zz_type[sub_key])
                    zz_content = zz_content.replace("['","")
                    zz_content = zz_content.replace("']","")
                    zz_content = zz_content.replace("', '"," ")
                    if ((sub_key == '@src' or sub_key == '@href') and (zz_content != "")):
                        if ( zz_content[0] == '/' ):
                            zz_content = url_1 + zz_content
                        elif ( zz_content[:4] != 'http' ):
                            zz_content = url_2 + zz_content
                    tag_name = tag_name + ' '
                    tag_name = tag_name + sub_key[1:] + '="'
                    tag_name = tag_name + zz_content + '"'
                else:
                    tag_page = tag_page + JSON2Html( sub_key, zz_type[sub_key] )
        outp = ' <' + tag_name + '> ' + tag_page + ' </' + key + '> '
        return outp
    if isinstance(zz_type, list):
        page = ''
        for sub_page in zz_type:
            page = page + JSON2Html( key, sub_page )
        return page
    return zz_decode( zz_type )

def genfile(url):
    global url_1
    global url_2
    conn = MongoClient('localhost')
    db = conn.html
    col = db.table
    dictVal = (col.find_one({"url":url}))
    #print dictVal

    #line = json.loads(l)
    #print line

    cutname = dictVal["url"].split('/')
    filename = cutname[-1]
    url_1 = cutname[0] + '//' + cutname[2]
    url_2 = dictVal["url"][:-len(cutname[-1])]
    if (dictVal['url'] == "http://electsys.sjtu.edu.cn"):
        url_2 = "http://electsys.sjtu.edu.cn/"
    del dictVal["url"]

    tag_name = 'html'
    the_page = JSON2Html( "head", dictVal['html']['head'])
    the_page = the_page + JSON2Html( "body", dictVal['html']['body'])
    for sub_key in dictVal['html']:
        if (sub_key[0] == '@'):
            tag_name = tag_name + ' '
            tag_name = tag_name + sub_key[1:] + '="'
            tag_name = tag_name + zz_decode(dictVal['html'][sub_key]) + '"'

    data = ' <' + tag_name + '> ' + the_page + ' </html> '
    data = data.encode('utf-8')

    f =  open("templates/"+filename, 'w')
    f.write(data)

if __name__ == "__main__":
    global url_1
    global url_2
    app.run('0.0.0.0',4576)
