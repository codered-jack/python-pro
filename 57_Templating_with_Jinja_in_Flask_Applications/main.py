# Blog Capstone Project Part 1

import datetime as dt

from flask import Flask, render_template
import requests

from post import Post

# Dummy blog post data.
JSON_URL = "https://api.npoint.io/9b81097a622d688871fa"

app = Flask(__name__)


def get_current_year() -> int:
    """Return current year to show in templates footer."""
    return dt.datetime.now().year


def fetch_posts():
    """Fetch posts from API and convert each item into a Post object."""
    response = requests.get(JSON_URL, timeout=15)
    response.raise_for_status()
    blog_posts = response.json()
    return [
        Post(
            id=item["id"],
            title=item["title"],
            subtitle=item["subtitle"],
            body=item["body"],
        )
        for item in blog_posts
    ]


# Load posts once when app starts.
ALL_POSTS = fetch_posts()
POSTS_BY_ID = {post.id: post for post in ALL_POSTS}


@app.route("/")
def home():
    return render_template("index.html", posts=ALL_POSTS, year=get_current_year())


@app.route("/blog/<int:blog_id>")
def get_blog(blog_id):
    # If blog_id does not exist, post is None and template shows fallback text.
    current_post = POSTS_BY_ID.get(blog_id)
    return render_template("post.html", post=current_post, year=get_current_year())

if __name__ == "__main__":
    app.run(debug=True)
