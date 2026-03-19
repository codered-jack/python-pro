# Blog Capstone Project Part 2

import datetime as dt

from flask import Flask, render_template
import requests

from post import Post

# Extended dummy blog post data.
JSON_URL = "https://api.npoint.io/fce4df05100e25cfbc7f"

app = Flask(__name__)


def get_current_year() -> int:
    """Return current year for footer rendering."""
    return dt.datetime.now().year


def load_posts():
    """Fetch posts and convert each JSON row into Post objects."""
    response = requests.get(JSON_URL, timeout=15)
    response.raise_for_status()
    blog_posts = response.json()
    return [
        Post(
            id=item["id"],
            author=item["author"],
            date=item["date"],
            title=item["title"],
            subtitle=item["subtitle"],
            image_url=item["image_url"],
            body=item["body"],
        )
        for item in blog_posts
    ]


# Load once at startup for this project scope.
ALL_POSTS = load_posts()
POSTS_BY_ID = {post.id: post for post in ALL_POSTS}


@app.route("/")
def home():
    return render_template("index.html", posts=ALL_POSTS, year=get_current_year())


@app.route("/about")
def about():
    return render_template("about.html", year=get_current_year())


@app.route("/contact")
def contact():
    return render_template("contact.html", year=get_current_year())


@app.route("/post/<int:blog_id>")
def get_post(blog_id):
    current_post = POSTS_BY_ID.get(blog_id)
    if current_post is None:
        return render_template("index.html", posts=ALL_POSTS, year=get_current_year())
    return render_template("post.html", post=current_post, year=get_current_year())

if __name__ == "__main__":
    app.run(debug=True)
