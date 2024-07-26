"""
Library Features:

Name:          lib_settings
Author(s):     Martina Natali
Date:          '20240212'
Version:       '1.0.0'
"""
# ----------------------------------------------------------------------------
# libraries
import os
import json
import logging
# ----------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# method to get data settings
def get_data_settings(file_name):
    if os.path.exists(file_name):
        with open(file_name) as file_handle:
            data_settings = json.load(file_handle)
    else:
        logging.error(' ===> Error in reading settings file "' + file_name + '"')
        raise IOError('File not found')
    return data_settings

# -------------------------------------------------------------------------------------

def substitute_keywords(template, **kwargs):
    for key, value in kwargs.items():
        template = template.replace('{' + key + '}', str(value))
    return template

# -------------------------------------------------------------------------------------