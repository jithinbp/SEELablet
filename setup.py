#!/usr/bin/env python

#from distutils.core import setup
from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.install import install
import os,shutil
from distutils.util import execute
from distutils.cmd import Command
from subprocess import call

def udev_reload_rules():
	call(["udevadm", "control", "--reload-rules"])

def udev_trigger():
	call(["udevadm", "trigger", "--subsystem-match=usb","--attr-match=idVendor=04d8", "--action=add"])

def install_udev_rules(raise_exception):
	if check_root():
		shutil.copy('proto.rules', '/etc/udev/rules.d')
		execute(udev_reload_rules, [], "Reloading udev rules")
		execute(udev_trigger, [], "Triggering udev rules")
	else:
		msg = "You must have root privileges to install udev rules. Run 'sudo python setup.py install'"
		if raise_exception:
			raise OSError(msg)
		else:
			print(msg)

def check_root():
	return os.geteuid() == 0

class CustomInstall(install):
        def run(self):
                if not hasattr(self,"root") or 'debian' not in self.root:
                        install_udev_rules(True)
                install.run(self)

data_files = []
def subdirs(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

try:
    directories=subdirs('docs/build/html/')
    directories.append('')
    for directory in directories:
        directory = 'docs/build/html/'+directory
        files = os.listdir(directory)
        files = [name for name in files	if not os.path.isdir(os.path.join(directory, name))]
        files = [os.path.join(directory,a) for a in files]
        data_files.append((directory,files))
except:
    pass

#print (data_files)

setup(name='SEEL',
	version='0.1',
	description='Package to deal with vLabtool-version 0',
	author='Jithin B.P.',
	author_email='jithinbp@gmail.com',
	url='https://vlabtool.jithinbp.in',
	install_requires = ['numpy>=1.8.1','pyqtgraph>=0.9.10'],
	packages=find_packages(),#['Labtools', 'Labtools.widgets'],
	scripts=["SEEL/bin/"+a for a in os.listdir("SEEL/bin/")],
	package_data={'': ['*.css','*.png','*.gif','*.html','*.css','*.js','*.png','*.jpg','*.jpeg','*.htm','proto.rules']},
	cmdclass={'install': CustomInstall},
	)
