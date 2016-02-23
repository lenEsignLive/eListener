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
import json
from google.appengine.ext import db

class Package(db.Model):
	id = db.StringProperty(required=True)
	status = db.StringProperty(required=True)

class eListener(webapp2.RequestHandler):
		
	def post(self):
		payload = self.request.body
		tokens = json.loads(payload)
		self.response.write('name "' + tokens['name'] +'"')
		p = Package(id=tokens['packageId'], status=tokens['name'])
		p.put()	
	
class MainHandler(webapp2.RequestHandler):

    def get(self):
		created = Package.gql("where status='PACKAGE_CREATE'")
		completed = Package.gql("where status='PACKAGE_COMPLETE'")
		declined = Package.gql("where status='PACKAGE_DECLINE'")
		self.response.write('<h1>e-Sign Live Listener Example</h1> packages created = ' + str(created.count()) + 
		'<br> packages completed = ' + str(completed.count()) + 
		'<br> packages  declined = ' + str(declined.count()))
		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/elistener', eListener)
], debug=True)
