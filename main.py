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


def build_page ():

    header = "<h1>Signup</h1>"

    username_label = "<label>Username</label>"
    username_input = "<input type=text name='username' required>"
    # username_error = "<font color='red'>That's not a valid username</font>"

    password_label = "<label>Password</label>"
    password_input = "<input type=text name='password' required>"
    # password_error = "<font color='red'>That's not a valid password</font>"

    verify_label = "<label>Verify Password</label>"
    verify_input = "<input type=text name='verify' required>"
    # verify_error = "<font color='red'>Passwords don't match</font>"

    email_label = "<label>Email (optional)</label>"
    email_input = "<input type=email name='email'>"
    # email_error = "<font color='red'>That's not a valid email</font>"

    submit = "<input type='submit'/>"

    # form = ("<form method='post'>" +
    #         username_label + "         " + username_input + username_error + "<br>" +
    #         password_label + "         " + password_input + password_error +  "<br>" +
    #         verify_label + "  " + verify_input + verify_error +  "<br>" +
    #         email_label + " " + email_input + email_error +  "<br><br>" +
    #         submit + "</form>")

    form = ("<form method='post'>" +
            username_label + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + username_input + "&nbsp;" + "<br>" +#username_error + "<br>" +
            password_label + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+ password_input + "&nbsp;" + "<br>" +#password_error +  "<br>" +
            verify_label + "&nbsp;"+ verify_input + "&nbsp;" + "<br>" +#verify_error +  "<br>" +
            email_label + "&nbsp;"+ email_input + "&nbsp;" + "<br><br>" +#email_error +  "<br><br>" +
            submit + "</pre></form>")


    return header + form


class MainHandler(webapp2.RequestHandler):

    def get(self):
        content = build_page()
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
