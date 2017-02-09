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


# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
</head>
<body>
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


def build_page (username, username_check, password, password_check, verify, verify_check, email, email_check):

    username_label = "<label>Username</label>"
    username_input = "<input type=text name='username' required>"
    if username_check:
        username_errortext = ""
    else:
        username_errortext = "<span style='color:red'>That's not a valid username</span>"

    password_label = "<label>Password</label>"
    password_input = "<input type=password name='password' required>"
    password_error = ""
    if password_check:
        password_errortext = ""
    else:
        password_errortext = "<span style='color:red'>That's not a valid password</span>"

    verify_label = "<label>Verify Password</label>"
    verify_input = "<input type=password name='verify' required>"
    verify_error = ""
    if verify_check:
        verify_errortext = ""
    else:
        verify_errortext = "<span style='color:red'>Passwords don't match</span>"

    email_label = "<label>Email (optional)</label>"
    email_input = "<input type=email name='email'>"
    if email_check:
        email_errortext = ""
    else:
        email_errortext = "<span style='color:red'>That's not a valid email</span>"

    submit = "<input type='submit'/>"

    form = ("<form method='post' action='/add'>" +
            "<table><tbody>" +
            "<tr><td>" + username_label + "</td><td>" + username_input + "</td><td>" + username_errortext + "</td></tr>" +
            "<tr><td>" + password_label + "</td><td>" + password_input + "</td><td>" + password_errortext + "</td></tr>" +
            "<tr><td>" + verify_label + "</td><td>" + verify_input + "</td><td>" + verify_errortext + "</td></tr>" +
            "<tr><td>" + email_label + "</td><td>" + email_input + "</td><td>" + email_errortext + "</td></tr>" +
            "</tbody></table>"+
            submit + "</form>.format")

    return form


class MainHandler(webapp2.RequestHandler):

    def get(self):

        #INIT CHECKS TRUE
        #username_check = True
        #password_check = True
        #verify_check = True
        #email_check = True

        #GET FIELD VALUES
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")


        username_check = self.request.get("username_check")
        if not username_check:
            username_check = True

        password_check = self.request.get("password_check")
        if not password_check:
            password_check = True

        verify_check = self.request.get("verify_check")
        if not verify_check:
            verify_check = True

        email_check = self.request.get("email_check")
        if not email_check:
            email_check = True

        #username = self.request.get("username")
        ###RELOAD FIELD EMPTY SO NO NEED PASS### password = self.request.get("password")
        ###RELOAD FIELD EMPTY SO NO NEED PASS### verify = self.request.get("verify")
        #email = self.request.get("email")


        self.response.write("username_check"+str(username)+str(username_check)+"<br>"+
                            "password_check"+str(password)+str(password_check)+"<br>"+
                            "verify_check"+str(verify)+str(verify_check)+"<br>"+
                            "email_check"+str(email)+str(email_check)+"<br>")

        page_content = build_page(username, username_check, password, password_check, verify, verify_check, email, email_check)
        content = page_header + "<h1>Signup</h1>"+page_content + page_footer
        self.response.write(content)


class AddUser(webapp2.RequestHandler):
    #HANDLES REQUESTS COMING IN TO '/add'

    def post(self):
        #INITIALIZE CHECKS TO TRUE
        username_check = True
        username_check_text = "True"
        password_check = True
        password_check_text = "True"
        verify_check = True
        verify_check_text = "True"
        email_check = True
        email_check_text = "True"

        #GETTING VALUES
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        #CHECKING VALIDITY OF VALUES
        if not valid_username(username):
            username_check = False
            username_check_text = "False"
        if not valid_password(password):
            password_check = False
            password_check_text = "False"
        if verify != password:
            verify_check = False
            verify_check_text = "False"
        if email and not valid_email(email):
            email_check = False
            email_check_text = "False"

        #BASED ON VALIDITY, DIRECT USER TO WELCOME OR REJECT
        if username_check and password_check and verify_check and email_check:
            #GO TO WELCOME
            self.redirect('/welcome?username=' + username)
        else:
            #RELOAD PAGE (APPROPRIATELY)
            self.redirect('/?username=' + username + '&username_check=' + username_check_text + '&password_check=' + password_check_text + '&verify_check=' + verify_check_text + '&email=' + email + '&email_check=' + email_check_text)


class Welcome(webapp2.RequestHandler):
    #HANDLES REQUESTS COMING IN TO '/welcome'
    def get(self):

        username = self.request.get("username")

        page_content ="<h1>" +"Welcome, " + username + "!</h1>"
        content = page_header + page_content + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add', AddUser),
    ('/welcome', Welcome)
], debug=True)
