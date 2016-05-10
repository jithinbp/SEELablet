DESTDIR =
all:
	make -C docs html
	#make -C docs/misc all
	# make in subdirectory SEELablet-apps-master if it is there
	[ ! -d SEELablet-apps-master ] || make -C SEELablet-apps-master $@ DESTDIR=$(DESTDIR)
	python setup.py build
	python3 setup.py build

clean:
	rm -rf docs/_*
	# make in subdirectory SEELablet-apps-master if it is there
	[ ! -d SEELablet-apps-master ] || make -C SEELablet-apps-master $@ DESTDIR=$(DESTDIR)
	rm -rf SEEL.egg-info build
	find . -name "*~" -o -name "*.pyc" -o -name "__pycache__" | xargs rm -rf

IMAGEDIR=$(DESTDIR)/usr/share/doc/seelablet-common/images

install:
	# make in subdirectory SEELablet-apps-master if it is there
	[ ! -d SEELablet-apps-master ] || make -C SEELablet-apps-master $@ DESTDIR=$(DESTDIR)
	# install documents
	install -d $(DESTDIR)/usr/share/doc/seelablet
	#[ -d ../SEELablet_Experiments ] && make -C ../SEELablet_Experiments $@ DESTDIR=$(DESTDIR)
	#cp -a docs/_build/html $(DESTDIR)/usr/share/doc/seelablet
	#cp docs/misc/build/*.html $(DESTDIR)/usr/share/doc/seelablet/html
	# create ditributions for Python2 and Python3
	python setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr
	python3 setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr
	# rules for udev
	mkdir -p $(DESTDIR)/lib/udev/rules.d
	install -m 644 proto.rules $(DESTDIR)/lib/udev/rules.d/99-seelablet
	# fix a few permissions
	find $(DESTDIR)/usr/share/seelablet/seel_res -name auto.sh -exec chmod -x {} \;
