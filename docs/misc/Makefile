DESTDIR =
SOURCES = $(shell ls *.html)
BUILDS  = $(patsubst %,build/%,$(SOURCES))

all: $(BUILDS)

build/%.html : %.html
	@mkdir -p build
	@./inline_images $<
	@echo "$< ==> $@"

clean:
	rm -f *~
	rm -f $(BUILDS)

install:
	install -m 644 $(BUILDS) $(DESTDIR)/docs/html

.PHONY: all clean install
