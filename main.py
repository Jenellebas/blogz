from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Launchcode1@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

def get_current_userlist():
    return User.query.all()


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog_list']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect ('/login')        

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        username_error = ""
        password_error = ""

        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')

        if user and user.password != password:
            password_error = "That is not a valid password."
            return render_template('login.html', username = username, password_error = password_error)
        else:
            flash('Username does not exist', 'error')
            return redirect('/login')
    
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')        

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify']

        username_error = ""
        password_error = ""
        verify_password_error = ""
        
        #if username is blank
        if username == "":
            username_error = "You must enter a username."
            username = ""

        #if username is less than 3 characters or more than 20
        if len(username) < 3 or len(username) > 20:
            username_error = "That is not a valid username."
            username = ""

        #if username has a space
        for char in username:
            if char == " ":
                username_error = "That is not a valid username."
                username = ""    

        #if password is blank
        if password == "":
            password_error = "You must enter a password."
            password = ""

        #if password is less than 3 characters or more than 20
        if len(password) < 3 or len(password) > 20:
            password_error = "That is not a valid password."
            password = ""

        #if password has a space
        for char in password:
            if char == " ":
                password_error = "That is not a valid password."
                password = ""    
        
        #if verify password is blank
        if verify_password == "":
            verify_password_error = "Passwords don't match."
            verify_password = ""

        #if password and verify password don't match
        if password != verify_password:
            verify_password_error = "Passwords don't match."
            verify_password = ""
            password = ""

        #if verify password is less than 3 characters or more than 20
        if len(verify_password) < 3 or len(verify_password) > 20:
            verify_password_error = "That is not a valid password."
            password = ""
        
            
        #check to see if any errors 
        if not username_error and not password_error and not verify_password_error:
            #check to see if username already exits
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                username_error = "That username already exists."
                username = ""
                return render_template('signup.html', username_error=username_error)
            
            #if doesn't exist, add new user
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost?username={0}'.format(username))

        else:
            return render_template('signup.html', username=username, username_error=username_error, password_error=password_error, verify_password_error=verify_password_error)



@app.route('/newpost', methods=['POST', 'GET'])
def add_post():

    if request.method == 'GET':
       return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog_list():

    title_error = ""
    body_error = ""

    if request.method == 'POST':
        blog_title = request.form['title']
        body_entry = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        new_entry = Blog(blog_title, body_entry, owner)

        #if title is blank
        if blog_title == "":
            title_error = "Please enter a title."
            blog_title = ""
        
        #if body is blank
        if body_entry == "":
            body_error = "Please enter a blog post."
            body_entry = ""

    #check to see if any errors 
        if not title_error and not body_error:
            db.session.add(new_entry)
            db.session.commit()
            blog2 = new_entry.id
            blog_id2 = str(blog2)
            return redirect('/blog?id='+ blog_id2)
        else:
            return render_template('newpost.html', title=blog_title, body=body_entry, owner=owner, title_error=title_error, body_error=body_error)

    if request.method == 'GET':

        if not request.args:
            blogs = Blog.query.all()
            #####username = User.username == blogs.owner_id
            return render_template('blog.html', title="Build A Blog", blogs=blogs)
            ###, username=username)
            
        else:
            blog_id = int(request.args.get('id'))
            blog = Blog.query.get(blog_id)
            title = blog.title
            body = blog.body
            owner = blog.owner_id
            return render_template('indivpost.html', title=title, body=body, owner=owner)


@app.route('/')
def index():
    list_of_owners = User.query.all()
    #each_owner_name = list_of_owners.username
    return render_template('index.html', owners=list_of_owners)

if __name__ == '__main__':
    app.run()