#!/usr/bin/env python

"""
Demonstrates:
   * Sharding - Sharding a counter into N random pieces
   * Memcache - Using memcache to cache the total counter value in generalcounter.
"""

import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import generalcounter
import simplecounter

class CounterHandler(webapp.RequestHandler):
  """
  Handles displaying the values of the counters
  and requests to increment either counter.
  """

  def get(self):
    template_values = {
      'simpletotal': simplecounter.get_count(),
      'generaltotal': generalcounter.get_count('Vote')
    }
    template_file = os.path.join(os.path.dirname(__file__), 'counter.html')
    self.response.out.write(template.render(template_file, template_values))

  def post(self):
    counter = self.request.get('counter')
    if counter == 'simple':
      simplecounter.increment()
    else:
      generalcounter.increment('Vote')
    self.redirect("/")


def main():
  application = webapp.WSGIApplication(
  [  
    ('/', CounterHandler),
  ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
