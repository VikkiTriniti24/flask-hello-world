from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

def fetch_post_by_id(post_id):
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None

@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_post = {
            'id': len(load_blog_posts()) + 1,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        blog_posts = load_blog_posts()
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        post['author'] = request.form['author']
        save_blog_posts(load_blog_posts())  # Speichere die aktualisierten Daten zurück
        return redirect(url_for('index'))

    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)




