# Flask HTML Forms

import datetime as dt
import smtplib

from flask import Flask, render_template, request
import requests

import config
from post import Post

# extended dummy blog post data
JSON_URL = "https://api.npoint.io/fce4df05100e25cfbc7f"
# default Mailtrap server settings
SMTP_SERVER = "smtp.mailtrap.io"
SMTP_PORT = "2525"
# not really necessary, but might as well format the email properly
SUBJECT_TEXT = "A Message from the Blog Capstone Project"
# fake contact info from Day 47
RECEIVER_NAME = "Anita Bath"
RECEIVER_ADDRESS = "myemail@mydomain.zyx"

app = Flask(__name__)


def get_current_year() -> int:
    """Return current year for template footer."""
    return dt.datetime.now().year


def load_posts():
    """Fetch posts from API and convert rows to Post objects."""
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


ALL_POSTS = load_posts()
POSTS_BY_ID = {post.id: post for post in ALL_POSTS}


def send_email(message: dict) -> bool:
    """Send contact form message and return success flag."""
    sender = f"{message['name']} <{message['email']}>"
    receiver = f"{RECEIVER_NAME} <{RECEIVER_ADDRESS}>"
    body = (
        f"Subject: {SUBJECT_TEXT}\nTo: {receiver}\nFrom: {sender}\n\n"
        f"{message['message']}\n\n"
        f"From:\nName: {message['name']}\nEmail: {message['email']}\nPhone: {message['phone']}"
    )
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_LOGIN, config.SMTP_PASS)
            server.sendmail(sender, receiver, body)
    except smtplib.SMTPServerDisconnected as ex:
        print(ex)
        print("Make sure the SMTP_LOGIN and SMTP_PASS credentials have been set correctly in config.py.")
        return False
    else:
        # just to have some feedback
        print(f"A message was sent to {RECEIVER_ADDRESS}.")
        return True


@app.route("/")
def home():
    return render_template("index.html", posts=ALL_POSTS, year=get_current_year())


@app.route("/about")
def about():
    return render_template("about.html", year=get_current_year())


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        message = {
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "message": request.form["message"]
        }
        if send_email(message):
            status = "Success!"
            text = "Your message has been sent."
        else:
            status = "Something went wrong."
            text = "The message could not be sent."
        return render_template("message.html", status=status, text=text)
    return render_template("contact.html", year=get_current_year())


@app.route("/post/<int:blog_id>")
def get_post(blog_id):
    current_post = POSTS_BY_ID.get(blog_id)
    if current_post is None:
        return render_template("index.html", posts=ALL_POSTS, year=get_current_year())
    return render_template("post.html", post=current_post, year=get_current_year())

if __name__ == "__main__":
    app.run(debug=True)
