#! /usr/bin/python3

import sys
from bs4 import BeautifulSoup as bs

with open(sys.argv[1]) as htmlIN, \
     open(sys.argv[2], "w") as htmlOUT, \
     open("insert.html") as ins:
    doc=bs(htmlIN, "lxml")
    insert=bs(ins, "lxml")
    ## add elements from insert.html into
    ## head section.
    header=doc.head
    for e in insert.head.children:
        header.append(e)
    ## all math elements should be inlined
    maths=doc.find_all("math")
    for math in maths:
        math["display"]="inline"
    ## add an anchor near table of contents
    tables=doc.find_all("table")
    toc=[t for t in tables if "Sect1" in t["class"]]
    if toc:
        soup = bs("<a name='toc'></a>", "lxml")
        anchor = soup.a
        toc[0].insert_before(anchor)
    ## add return buttons near every header (h1, h2)
    h1=doc.find_all("h1")
    h2=doc.find_all("h2")
    for h in h1 + h2:
        soup=bs("<a href='#toc' class='retButton'>↸</a>", "lxml")
        button=soup.a
        h.insert_after(button)
    ## output the modified document
    htmlOUT.write(doc.prettify())

