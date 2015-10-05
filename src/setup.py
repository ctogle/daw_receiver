#!/usr/bin/python
from os.path import isfile, join
import glob
import os
import re

import appdirs

from setuptools import setup#, Extension

import pdb

if isfile("MANIFEST"):
    os.unlink("MANIFEST")

TOPDIR = os.path.dirname(__file__) or "."
#VERSION = re.search('__version__ = "([^"]+)"',
#	open(TOPDIR + "/src/pkg1/__init__.py").read()).group(1)
VERSION = '1.0'

core_modules = [
	'modular_dr.libdawcontrol', 
	'modular_dr.libphidgmotor', 

	'modular_dr.gui.libqtgui_daw_receiver', 
				]

def ignore_res(f):
	#if f.startswith('__') or f.startswith('_.'): return True
	#else: return False
	if f.endswith('.txt'): return False
	elif f.endswith('.log'): return False
	else: return True

res_dir = 'modular_dr/resources/'
res_fis = [f for f in os.listdir(os.path.join(
	os.getcwd(), 'modular_dr', 'resources')) 
			if not ignore_res(f)]
res_files = [res_dir + f for f in res_fis]

requirements = [
	'modular_core >= 1.0', 
			]

setup(
	name="modular_daw_receiver-pkg",
	version = VERSION,
	description = "modular daw receiver pkg",
	author = "ctogle",
	author_email = "cogle@vt.edu",
	url = "http://github.com/ctogle/daw_receiver",
	license = "MIT License",
	long_description =
"""\
This is the daw receiver program of modular
""",
	#install_requires = requirements, 
	#scripts = [], 
	packages = ['modular_dr', 'modular_dr.gui'], 
	py_modules = core_modules, 
	zip_safe = False,
	data_files=[(os.path.join(appdirs.user_config_dir(), 
		    'modular_resources'), res_files)], 
	)

