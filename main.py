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
import re
import cgi

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
</head>
<body>
    <h1>Signup</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)


def build_page (username_check, password_check, verify_check, email_check):

    username_label = "<label>Username</label>"
    username_input = "<input type=text name='username' required>"
    if username_check:
        username_error = ""
    else:
        username_error = "<font color='red'>That's not a valid username</font>"

    password_label = "<label>Password</label>"
    password_input = "<input type=text name='password' required>"
    password_error = ""
    #password_error = "<font color='red'>That's not a valid password</font>"

    verify_label = "<label>Verify Password</label>"
    verify_input = "<input type=text name='verify' required>"
    verify_error = ""
    #verify_error = "<font color='red'>Passwords don't match</font>"

    email_label = "<label>Email (optional)</label>"
    email_input = "<input type=email name='email'>"
    email_error = ""
    #email_error = "<font color='red'>That's not a valid email</font>"

    submit = "<input type='submit'/>"

    form = ("<form method='post' action='/add'>" +
            "<table><tbody>" +
            "<tr><td>" + username_label + "</td><td>" + username_input + "</td><td>" + username_error + "</td></tr>" +
            "<tr><td>" + password_label + "</td><td>" + password_input + "</td><td>" + password_error + "</td></tr>" +
            "<tr><td>" + verify_label + "</td><td>" + verify_input + "</td><td>" + verify_error + "</td></tr>" +
            "<tr><td>" + email_label + "</td><td>" + email_input + "</td><td>" + email_error + "</td></tr>" +
            "</tbody></table>"+
            submit + "</form>")

    return form


class MainHandler(webapp2.RequestHandler):

    def get(self):

        username_check = True
        password_check = True
        verify_check = True
        email_check = True
        page_content = build_page(username_check, password_check, verify_check, email_check)
        content = page_header + page_content + page_footer
        self.response.write(content)


class AddUser(webapp2.RequestHandler):
    #HANDLES REQUESTS COMING IN TO '/add'

    def post(self):
        #INITIALIZE CHECKS TO TRUE
        username_check = True
        password_check = True
        verify_check = True
        email_check = True

        #GETTING VALUES
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        #CHECKING VALIDITY OF VALUES
        if not valid_username(username):
            username_check = False
        if not valid_password(password):
            password_check = False
        if verify != password:
            verify_check = False
        if email and not valid_email(email):
            email_check = False

        #BASED ON VALIDITY, DIRECT USER TO WELCOME OR REJECT
        if username_check and password_check and verify_check and email_check:
            #GO TO WELCOME
            #self.redirect('/welcome')
            self.redirect('/welcome?username=' + username)
            #self.response.write("submit check pass")
        else:
            #RELOAD PAGE (APPROPRIATELY)
            the_form = cgi.FieldStorage()
            self.redirect('/')
            #self.response.write("username_check"+str(username_check)+"<br>"+"password_check"+str(password_check)+"<br>"+"verify_check"+str(verify_check)+"<br>""email_check"+str(email_check)+"<br>") #self.response.write("submit error")


class Welcome(webapp2.RequestHandler):
    #HANDLES REQUESTS COMING IN TO '/welcome'
    def get(self):
        #content ="<h2>" +"Welcome " + "</h2>"
        username = self.request.get("username")
        content ="<h2>" +"Welcome " + username + "</h2>"
        self.response.write(content)
        #self.response.write("Hello welcome")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add', AddUser),
    ('/welcome', Welcome)
], debug=True)
