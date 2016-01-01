DESTDIR =
all:
	make -C docs html
	make -C docs/misc all
	python setup.py build
	python3 setup.py build

clean:
	rm -rf SEEL.egg-info build
	find . -name "*~" -o -name "*.pyc" -o -name "__pycache__" | xargs rm -rf
	make -C docs clean
	make -C docs/misc clean

IMAGEDIR=$(DESTDIR)/usr/share/doc/seelablet-common/images

install:
	# install documents
	install -d $(DESTDIR)/usr/share/doc/seelablet
	cp -a docs/build/html $(DESTDIR)/usr/share/doc/seelablet
	cp docs/misc/build/*.html $(DESTDIR)/usr/share/doc/seelablet/html
	# create ditributions for Python2 and Python3
	python setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr
	python3 setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr
	# move png files from dist-package dirs to /usr/share
	for d in stylesheets controls apps; do \
	  mkdir -p $(IMAGEDIR)/$$d; \
	  mv $(DESTDIR)/usr/lib/python2.7/dist-packages/SEEL/$$d/*.png $(IMAGEDIR)/$$d; \
	  rm -f $(DESTDIR)/usr/lib/python3/dist-packages/SEEL/$$d/*.png; \
	  for f in $(IMAGEDIR)/$$d/*.png; do \
	    ln -rs $$f $(DESTDIR)/usr/lib/python2.7/dist-packages/SEEL/$$d/ ; \
	    ln -rs $$f $(DESTDIR)/usr/lib/python3/dist-packages/SEEL/$$d/ ; \
	  done; \
	done
	# rules for udev
	mkdir -p $(DESTDIR)/lib/udev/rules.d
	install -m 644 proto.rules $(DESTDIR)/lib/udev/rules.d/99-seelablet
