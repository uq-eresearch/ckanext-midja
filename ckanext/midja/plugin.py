import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def create_data_types():
    '''Create data_types vocab and tags, if they don't exist already.

    Note that you could also create the vocab and tags using CKAN's API,
    and once they are created you can edit them (e.g. to add and remove
    possible values) using the API.

    '''
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'data_types'}
        toolkit.get_action('vocabulary_show')(context, data)
        logging.info("Example data_types vocabulary already exists, skipping.")
    except toolkit.ObjectNotFound:
        logging.info("Creating vocab 'data_types'")
        data = {'name': 'data_types'}
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in (u'quantitative-data', u'report', u'qualitative-survey', u'qualitative-longitudinal-study', u'qualitative-case-study', u'geospatial-data'):
            logging.info(
                    "Adding tag {0} to vocab 'data_types'".format(tag))
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)
    try:
        geographies = {'id': 'geographies'} 
        toolkit.get_action('vocabulary_show')(context, geographies)
        logging.info("Example geographies vocabulary already exists, skipping.")
    except toolkit.ObjectNotFound:  
        logging.info("Creating vocab 'geographies'")
        data = {'name': 'data_types'}
        vocab = toolkit.get_action('vocabulary_create')(context, geographies)
        for tag in (u'LGA',u'SLA',u'IA',u'ML'):
            logging.info(
                    "Adding tag {0} to vocab 'geographies'".format(tag))
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)

def data_types():
    '''Return the list of terms from the data types vocabulary.'''
    create_data_types()
    try:
        return toolkit.get_action('tag_list')(
                data_dict={'vocabulary_id': 'data_types'})
    except toolkit.ObjectNotFound:
        return None
def geographies():
    '''Return the list of terms from the geographies vocabulary.'''
    create_data_types()
    try:
        return toolkit.get_action('tag_list')(
                data_dict={'vocabulary_id': 'geographies'})
    except toolkit.ObjectNotFound:
        return None


class MidjaPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_resource('fantastic','midja')

    def get_helpers(self):
        return {'data_types': data_types, 'geographies': geographies}

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def _modify_package_schema(self, schema):
        # Add our custom data_types metadata field to the schema.
        schema.update({
                'data_type': [toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_tags')('data_types')]
                })
        # Add our custom geographies metadata field to the schema.
        schema.update({
                'geography': [toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_tags')('geographies')]
                })
        # Add source_url and date fields to the schema
        schema.update({
                'source_url': [toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_extras')]
                })
        schema.update({
                'date': [toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_extras')]
                })

        return schema


    def create_package_schema(self):
        schema = super(MidjaPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(MidjaPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(MidjaPlugin, self).show_package_schema()

        # Don't show vocab tags mixed in with normal 'free' tags
        # (e.g. on dataset pages, or on the search page)
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))

        # Add our custom fields to the schema.
        schema.update({
            'data_type': [
                toolkit.get_converter('convert_from_tags')('data_types'),
                toolkit.get_validator('ignore_missing')]
            })
        schema.update({
            'geography': [
                toolkit.get_converter('convert_from_tags')('geographies'),
                toolkit.get_validator('ignore_missing')]
            })

        schema.update({
            'source_url': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })

        schema.update({
            'date': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })

        return schema

