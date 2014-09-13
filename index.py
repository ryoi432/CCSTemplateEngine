#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
#import cgitb
#cgitb.enable()

import sys
import os
import cgi

from mako.lookup import TemplateLookup
from mako import exceptions

sys.stderr = sys.stdout

print "Content-Type: text/html;charset=utf-8"
print

templatedir = "./template"
templatename = "test.template"

tl = TemplateLookup(directories=templatedir, output_encoding='utf-8', input_encoding='utf-8', encoding_errors='replace')

try:
	t = tl.get_template(templatename)
except exceptions.TopLevelLookupException, tlle:
	print >>sys.stderr ,'We could not find the template directory. - %s/%s'% (templatedir, templatename)
	raise

query_string_key = 'QUERY_STRING'
if query_string_key in os.environ:
	query = cgi.parse_qs(os.environ[query_string_key])
else:
	query = {}

message_key = 'path'
if message_key in query:
	filepath = cgi.escape(query[message_key][0])
else:
	filepath = "index.html"

filepath = os.path.abspath(os.path.join("./data/", filepath))
datadir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/'))

if not os.path.exists(filepath) or filepath.find(datadir) != 0:
	print u"404"
	sys.exit()

f = open(filepath)
body_data = f.read()
body_data = body_data.decode('utf-8')
f.close()

view = {"title" : os.path.basename(filepath), "body": body_data}
print t.render(**view)
