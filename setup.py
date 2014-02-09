from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(
	name='ckanext-midja',
	version=version,
	description="CKAN theme for Midja Data Registry",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Anna Gerber',
	author_email='',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.midja'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
    midja=ckanext.midja.plugin:MidjaPlugin
	""",
)
