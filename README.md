ckanext-midja
=============

CKAN theme for Midja Data Registry

To install, activate your CKAN virtualenv then run:

    pip install -e 'git+git://github.com/uq-eresearch/ckanext-midja.git#egg=ckanext-midja'

Then add the plugin to your CKAN config file (e.g. `development.ini` or
`production.ini`), for example:

  ckan.plugins = stats text_preview recline_preview midja