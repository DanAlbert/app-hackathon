#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

import os

import auth
from models import Idea, Project

from google.appengine.ext.webapp import template


def render_template(name, data):
    BASE_DIR = os.path.dirname(__file__)
    TEMPLATE_DIR = 'templates'
    path = os.path.join(BASE_DIR, TEMPLATE_DIR, "%s.html" % name)
    return template.render(path, data)


class ProjectsHandler(webapp2.RequestHandler):
    def get(self):
        (login_text, login_url) = auth.login_logout(self.request)
        data = {
            'projects': Project.all(),
            'admin': auth.user_is_admin(),
            'login_url': login_url,
            'login_text': login_text,
        }

        return self.response.out.write(render_template('projects', data))


class ProjectsDeleteHandler(webapp2.RequestHandler):
    def post(self, key):
        if auth.user_is_admin():
            Project.get(key).delete()
            return self.redirect('/projects')
        else:
            return self.abort(401)
    
    
class ProjectsVoteHandler(webapp2.RequestHandler):
    def post(self, key):
        if not auth.logged_in():
            return self.redirect('/projects')
        project = Project.get(key)
        if project.has_voted(auth.current_user()):
            project.remove_vote(auth.current_user())
        else:
            project.vote(auth.current_user())
        return self.redirect('/projects')
        
        
class IdeasHandler(webapp2.RequestHandler):
    def get(self):
        (login_text, login_url) = auth.login_logout(self.request)
        data = {
            'ideas': Idea.all(),
            'admin': auth.user_is_admin(),
            'login_url': login_url,
            'login_text': login_text,
        }

        return self.response.out.write(render_template('ideas', data))
    
    def post(self):
        name = self.request.get('name')
        description = self.request.get('description')
        Idea(name=name,
            description=description,
            author=auth.current_user()).put()
        return self.redirect('/ideas')


class IdeasApproveHandler(webapp2.RequestHandler):
    def post(self, key):
        if auth.user_is_admin():
            idea = Idea.get(key)
            Project(name=idea.name,
                    description=idea.description,
                    author=idea.author,
                    post_time=idea.post_time).put()
            idea.delete()
            return self.redirect('/projects')
        else:
            return self.abort(401)


class IdeasDeleteHandler(webapp2.RequestHandler):
    def post(self, key):
        if auth.user_is_admin():
            Idea.get(key).delete()
            return self.redirect('/ideas')
        else:
            return self.abort(401)

class LiveHandler(webapp2.RequestHandler):
    def get(self):
        (login_text, login_url) = auth.login_logout(self.request)
        data = {
            'ideas': Idea.all(),
            'admin': auth.user_is_admin(),
            'login_url': login_url,
            'login_text': login_text,
        }

        return self.response.out.write(render_template('live', data))


class AboutHandler(webapp2.RequestHandler):
    def get(self):
        (login_text, login_url) = auth.login_logout(self.request)
        data = {
            'ideas': Idea.all(),
            'admin': auth.user_is_admin(),
            'login_url': login_url,
            'login_text': login_text,
        }

        return self.response.out.write(render_template('about', data))


class FAQHandler(webapp2.RequestHandler):
    def get(self):
        (login_text, login_url) = auth.login_logout(self.request)
        data = {
            'ideas': Idea.all(),
            'admin': auth.user_is_admin(),
            'login_url': login_url,
            'login_text': login_text,
        }

        return self.response.out.write(render_template('faq', data))


app = webapp2.WSGIApplication([
    ('/', ProjectsHandler),
    ('/projects', ProjectsHandler),
    ('/projects/delete/(.*)', ProjectsDeleteHandler),
    ('/projects/vote/(.*)', ProjectsVoteHandler),
    ('/ideas', IdeasHandler),
    ('/ideas/approve/(.*)', IdeasApproveHandler),
    ('/ideas/delete/(.*)', IdeasDeleteHandler),
    ('/live', LiveHandler),
    ('/about', AboutHandler),
    ('/faq', FAQHandler),
], debug=True)
