from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


def load_blog_posts():
    """Load all blog posts from the JSON file."""
    if not os.path.exists('blog_posts.json'):
        return []
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def save_blog_posts(posts):
    """Save all blog posts to the JSON file."""
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    """Display all blog posts."""
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new blog post."""
    if request.method == 'POST':
        blog_posts = load_blog_posts()
        new_id = max((post['id'] for post in blog_posts), default=0) + 1
        new_post = {
            'id': new_id,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update a blog post by ID."""
    blog_posts = load_blog_posts()
    post = next((p for p in blog_posts if p['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        post['author'] = request.form['author']
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Delete a blog post by ID."""
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)





