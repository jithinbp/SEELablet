#! /usr/bin/python3

import sys
from bs4 import BeautifulSoup

with open(sys.argv[1]) as htmlIN, \
     open(sys.argv[2], "w") as htmlOUT, \
     open("insert.html") as ins:
    doc=BeautifulSoup(htmlIN, "lxml")
    insert=BeautifulSoup(ins, "lxml")
    header=doc.head
    for e in insert.head.children:
        header.append(e)
    maths=doc.find_all("math")
    for math in maths:
        math["display"]="inline"
    htmlOUT.write(str(doc))

