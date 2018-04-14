from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Launchcode1@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))

    def __init__(self, title, body):
        self.title = title
        self.body = body

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
        new_entry = Blog(blog_title, body_entry)

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
            blogs = Blog.query.all()
            return render_template('blog.html', title="Build A Blog", 
                blogs=blogs)
        else:
            return render_template('newpost.html', title=blog_title, body=body_entry, title_error=title_error, body_error=body_error)

    if request.method == 'GET':

        if not request.args:
            blogs = Blog.query.all()
            return render_template('blog.html', title="Build A Blog", 
            blogs=blogs)
            
            #return redirect('/blog')
            
        else:
            blog_id = int(request.args.get('id'))
            blog = Blog.query.get(blog_id)
            title = blog.title
            body = blog.body
            return render_template('indivpost.html', title=title, body=body)

if __name__ == '__main__':
    app.run()