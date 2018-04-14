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

    if request.method == 'POST':
        blog_title = request.form['title']
        body_entry = request.form['body']
        new_entry = Blog(blog_title, body_entry)
        db.session.add(new_entry)
        db.session.commit()

    blogs = Blog.query.all()
    return render_template('newpost.html', title="Build A Blog", blogs=blogs)

    if request.method == 'GET':
        return redirect('/blog')


@app.route('/blog', methods=['POST', 'GET'])
def blog_list():

    if request.method == 'POST':
        blog_title = request.form['title']
        body_entry = request.form['body']
        new_entry = Blog(blog_title, body_entry)
        db.session.add(new_entry)
        db.session.commit()

    blogs = Blog.query.all()
    return render_template('blog.html', title="Build A Blog!", 
        blogs=blogs)

if __name__ == '__main__':
    app.run()