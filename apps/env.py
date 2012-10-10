'''
Created on Oct 9, 2012

@author: Dan
'''
import os

def is_gae():
    if (os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine') or
            'Development' in os.getenv('SERVER_SOFTWARE', '') or
            os.getenv('SETTINGS_MODE') == 'prod'):
        return True
    else:
        return False

def is_gae_dev():
    return 'Development' in os.getenv('SERVER_SOFTWARE', '')