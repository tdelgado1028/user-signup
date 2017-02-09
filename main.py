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
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style type='text/css'>
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <div href='/'>Signup</div>
    </h1>
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
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):

    def get(self):

        #GET FIELD VALUES
        username = self.request.get("username")
        username_error = self.request.get("username_error")
        password_error = self.request.get("password_error")
        verify_error = self.request.get("verify_error")
        email = self.request.get("email")
        email_error = self.request.get("email_error")

        add_form="""
        <form action='/add' method='post'>
        <table><tbody>
        <tr><td>    <label for='username'>Username</label>      </td><td> <input name='username' type=text value="{0}" required>  <span class='error'>{1}</span> </td></tr>
        <tr><td>    <label for='password'>Password</label>      </td><td> <input name='password' type=password value required>    <span class='error'>{2}</span> </td></tr>
        <tr><td>    <label for='verify'>Verify Password</label> </td><td> <input name='verify' type=password value required>      <span class='error'>{3}</span> </td></tr>
        <tr><td>    <label for='email'>Email (optional)</label> </td><td> <input name='email' type=email value="{4}">             <span class='error'>{5}</span> </td></tr>
        </tbody></table>
        <input type='submit' value='Submit'/>
        </form>

        """.format(username, username_error, password_error, verify_error, email, email_error)

        content = page_header + add_form + page_footer
        self.response.write(content)


class AddUser(webapp2.RequestHandler):
    #HANDLES REQUESTS COMING IN TO '/add'
    def post(self):
        #self.response.write("values checked, 'Welcome, user'")
        input_errors = False

        #GETTING VALUES
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        #CHECKING VALIDITY OF VALUES
        if not valid_username(username):
            input_errors = True
            username_error = "That's not a valid username"
        if not valid_password(password):
            input_errors = True
            password_error = "That's not a valid password"
        if verify != password:
            input_errors = True
            verify_error = "Passwords don't match"
        if not valid_email(email):
            input_errors = True
            email_error = "That's not a valid email"

        #BASED ON VALIDITY, DIRECT USER TO WELCOME OR REJECT
        if input_errors:
            #RELOAD PAGE (APPROPRIATELY)
            self.redirect('/?username=' + username + '&username_error=' + username_error + '&password_error=' + password_error + '&verify_error=' + verify_error + '&email=' + email + '&email_error=' + email_error)
        else:
            #GO TO WELCOME
            self.redirect('/welcome?username=' + username)


class Welcome(webapp2.RequestHandler):
    #HANDLES REQUESTS COMING IN TO '/welcome'
    def get(self):

        username = self.request.get("username")

        content = "<h1>" +"Welcome, " + username + "!</h1>"
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add', AddUser),
    ('/welcome', Welcome)
], debug=True)
