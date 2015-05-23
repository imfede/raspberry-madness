#!/usr/bin/python3

import json
from pprint import pprint

jfile = open( 'notes.json', 'r')
data = json.load( jfile )
jfile.close()

flag = True
tune = []
while flag:
    a = input()
    a = a.split(" ")
    try:
        tune.append( [ int(data[a[0]]), float(a[1]) ] )
    except KeyError:
        flag = False

pprint( tune, indent=2, width=20, depth=4 )
