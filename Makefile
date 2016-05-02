DESTDIR =
all:
	make -C docs html
	#make -C docs/misc all
	make -C SEEL $@ DESTDIR=$(DESTDIR)
	python setup.py build
	python3 setup.py build

clean:
	rm -rf docs/_*
	make -C SEEL $@ DESTDIR=$(DESTDIR)
	rm -rf SEEL.egg-info build
	find . -name "*~" -o -name "*.pyc" -o -name "__pycache__" | xargs rm -rf

IMAGEDIR=$(DESTDIR)/usr/share/doc/seelablet-common/images

install:
	#make -C SEEL $@ DESTDIR=$(DESTDIR)
	# install documents
	#install -d $(DESTDIR)/usr/share/doc/seelablet
	#cp -a docs/build/html $(DESTDIR)/usr/share/doc/seelablet
	#cp docs/misc/build/*.html $(DESTDIR)/usr/share/doc/seelablet/html
	# create ditributions for Python2 and Python3
	python setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr
	python3 setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr
	# rules for udev
	mkdir -p $(DESTDIR)/lib/udev/rules.d
	install -m 644 proto.rules $(DESTDIR)/lib/udev/rules.d/99-seelablet
