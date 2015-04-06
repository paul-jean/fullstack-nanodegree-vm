#!/usr/bin/python

import cgi
import cgitb
import re
import sys
cgitb.enable()

sys.path.insert(0, "/vagrant/restaurant")
import restaurant_queries
from restaurant_queries import add_restaurant, restaurant_exists

form = cgi.FieldStorage()
restaurant_name = form["rest_name"].getvalue("_none_")
print "<p>Restaurant name entered: %s</p>" % restaurant_name
exists = restaurant_exists(restaurant_name)
print "<p>Already in the db?: %s</p>" % exists
if restaurant_name != "_none_" and re.match("[A-Za-z0-9' ]+", restaurant_name) != None:
    print "<p>Adding restaurant %s ...</p>" % restaurant_name
    add_restaurant(restaurant_name)
print """<a href="/restaurants">Back to restaurants</a>"""
