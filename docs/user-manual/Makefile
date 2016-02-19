DESTDIR =

###############################################################
# BUILD DEPENDENCIES
###############################################################
# odt2xhtml comes from the package python-odf-tools
###############################################################

SOURCES = $(shell ls manual*.odt)
TARGETS = $(patsubst manual%.odt, manual%.html, $(SOURCES))

all: $(TARGETS)

manual%tmp.html: manual%.odt insert.html insert.py
	odt2xhtml $<  && mv $$(echo $< | sed 's/\.odt$$/.html/') $@
manual%.html: manual%tmp.html
	insert.py $< $@  #inserts a few lines into the HTML

clean:
	rm -f $(TARGETS) *~

install:

.PHONY: all clean install
