import webapp2
import jinja2
import os
import re
import logging

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
        
    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))    
        
class SignupForm(Handler):
    def get(self):
        errormap = {}
        self.render('index.html',errormap=errormap,output={})
        
    def post(self):
        errormap = {}
        username = self.request.get('username')
        self.validateUsername(username,errormap)
        
        password = self.request.get('password')
        self.validatePassword(password,errormap)
        
        confirmpass = self.request.get('confirmpass')
        self.validateConfirmPass(password,confirmpass,errormap)
        
        email = self.request.get('email')
        self.validateEmail(email,errormap)
        logging.debug(errormap)
        if errormap:
            self.render('index.html',errormap=errormap,output={'username':username,'email':email})
        else:
            self.redirect('/welcome?username='+username)
    
    def validateUsername(self,username,errormap):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        logging.debug("Test Vlaid User %s",USER_RE.match(username))
        if not username or (username and not USER_RE.match(username)):
            errormap['username']="UserName is Invalid"
            
    def validatePassword(self,password,errormap):
        PASS_RE = re.compile(r".{3,20}$")
        if not password or (password and not PASS_RE.match(password)):
            errormap['password']="Password is Invalid"

    def validateConfirmPass(self,password,confirmpass,errormap):
        PASS_RE = re.compile(r".{3,20}$")
        if (password != confirmpass):
            errormap['confirmpassword']="Confirm Password is Invalid"

    def validateEmail(self,email,errormap):
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if email and not EMAIL_RE.match(email):
            errormap['email']="Email is Invalid"
        
class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get('username')
        self.render('welcome.html',username=username)

app = webapp2.WSGIApplication([
('/signup', SignupForm),('/welcome', WelcomeHandler),
], debug=True)
