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
import os
import webapp2
import jinja2
import json
import logging
import random
from Engine import *

myEngine = Engine()
myEngine.points.extend([
    Point(1000.0, 1000.0), Point(-1000.0, 1000.0), Point(-1000.0, -1000.0), Point(1000.0, -1000.0)    
]);
myEngine.edges.extend([
    Edge(myEngine.points[0], myEngine.points[1], "#000000"),
    Edge(myEngine.points[1], myEngine.points[2], "#000000"),
    Edge(myEngine.points[2], myEngine.points[3], "#000000"),
    Edge(myEngine.points[3], myEngine.points[0], "#000000")
]);
#myEngine.unPause()

def generateHTMLColor(r,g,b):
    rString = hex(r)[2:]
    gString = hex(g)[2:]
    bString = hex(b)[2:]
    return '#'+rString + gString + bString

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('html/game.html')
        self.response.write(template.render(template_values))

class SendEdges(webapp2.RequestHandler):
    def get(self):
        global myEngine
        edgeList = []
        for e in myEngine.edges:
            edgeList.append(e.toJSON())
        self.response.write(json.dumps(edgeList))

class SendBalls(webapp2.RequestHandler):
    def get(self):
        global myEngine
        myEngine.updateState()
        ballList = []
        for b in myEngine.circles:
            ballList.append(b.toJSON())
        self.response.write(json.dumps(ballList))

class TogglePause(webapp2.RequestHandler):
    def post(self):
        global myEngine
        if (myEngine.isPaused):
            myEngine.unPause()
        else:
            myEngine.pause()
        
class AddBall(webapp2.RequestHandler):
    def post(self):
        global myEngine
        c = Point(random.random()*1800-900, random.random()*1800-900)
        color = generateHTMLColor(random.randint(0,255), random.randint(0,255), random.randint(0,255))  #"#0000ff"
        newBall = Circle(c, random.random()*50 + 10, color)
        newBall.velocity.pf.x += random.random()*500 - 250
        newBall.velocity.pf.y += random.random()*500 - 250
        myEngine.circles.append(newBall)

class Reset(webapp2.RequestHandler):
    def get(self):
        global myEngine
        myEngine.circles = []
        edgeList = []
        for e in myEngine.edges:
            edgeList.append(e.toJSON())
        self.response.write(json.dumps(edgeList))        
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/uploadEdges', SendEdges),
    ('/uploadBalls', SendBalls),
    ('/togglePause', TogglePause),
    ('/addBall', AddBall),
    ('/reset', Reset)
], debug=True)
