'''
Created on Oct 9, 2012

@author: Dan
'''
from google.appengine.api import users

def current_user():
    return users.get_current_user()

def user_is_admin():
    return users.is_current_user_admin()

def logged_in():
    return current_user() is not None

def login_logout(request):
    if logged_in():
        url = users.create_logout_url(request.uri)
        text = 'Logout'
    else:
        url = users.create_login_url(request.uri)
        text = 'Login'
        
    return (text, url)