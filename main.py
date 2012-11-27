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
"""Entry point for the app-hackathon software.

Author: Dan Albert <dan@gingerhq.net>

Defines application routes and controllers.
"""
import webapp2

import os

import auth
import settings
from models import Idea, Project

from google.appengine.ext.webapp import template


def render_template(name, data):
    """Renders a template by name.

    Arguments:
        name: the name of the template. this is the file name of the template
              without the .html extension.

        data: a dictionary containing data to be passed to the template.
    """
    path = os.path.join(settings.BASE_DIR, settings.TEMPLATE_DIR,
                        "%s.html" % name)

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

    def vote(self, key):
        if not auth.logged_in():
            return self.redirect('/projects')
        project = Project.get(key)
        if project.has_voted(auth.current_user()):
            project.remove_vote(auth.current_user())
        else:
            project.vote(auth.current_user())
        return self.redirect('/projects')

    def delete(self, key):
        if auth.user_is_admin():
            Project.get(key).delete()
            return self.redirect('/projects')
        else:
            return self.abort(401)


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

    def approve(self, key):
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

    def delete(self, key):
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
    webapp2.Route(r'/projects/delete/<key>', name='projects_delete',
                  handler=ProjectsHandler, handler_method='delete'),
    webapp2.Route(r'/projects/vote/<key>', name='projects_vote',
                  handler=ProjectsHandler, handler_method='vote'),
    ('/ideas', IdeasHandler),
    webapp2.Route(r'/ideas/approve/<key>', name='ideas_approve',
                  handler=IdeasHandler, handler_method='approve'),
    webapp2.Route(r'/ideas/delete/<key>', name='ideas_delete',
                  handler=IdeasHandler, handler_method='delete'),
    ('/live', LiveHandler),
    ('/about', AboutHandler),
    ('/faq', FAQHandler),
], debug=True)
