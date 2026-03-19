# Flask-WTF Forms

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap

# Fake credentials for demo login.
SECRET_EMAIL = "myemail@mydomain.zyx"
SECRET_PASSWORD = "123123"
SECRET_KEY = "ThisIsASecretKey"

app = Flask(__name__)
app.secret_key = SECRET_KEY
Bootstrap(app)


class LoginForm(FlaskForm):
    """Login form with basic validation."""

    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField(label="Submit")


def is_valid_credentials(email: str, password: str) -> bool:
    """Return True when submitted credentials match expected values."""
    return email == SECRET_EMAIL and password == SECRET_PASSWORD


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if is_valid_credentials(form.email.data, form.password.data):
            return render_template("success.html")
        return render_template("denied.html")
    return render_template("login.html", login_form=form)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
