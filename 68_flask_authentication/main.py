# Flask Authentication

# Note: login credentials for user #1
# myemail@mydomain.zyx
# mypassword

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

SECRET_KEY = "ThisIsASecretKey"
DATABASE_URI = "sqlite:///users.db"

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# create a Flask login manager
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        found_user = User.query.filter_by(email=request.form.get("email")).first()
        if found_user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))

        password_hash = generate_password_hash(
            password=request.form.get("password"),
            method="pbkdf2:sha256",
            salt_length=8,
        )
        new_user = User(
            email=request.form.get("email"),
            password=password_hash,
            name=request.form.get("name"),
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("secrets"))
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        found_user = User.query.filter_by(email=request.form.get("email")).first()
        if found_user:
            verified = check_password_hash(pwhash=found_user.password, password=request.form.get("password"))
            if verified:
                login_user(found_user)
                return redirect(url_for("secrets"))
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))

        flash("Email not found, please try again.")
        return redirect(url_for("login"))
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/secrets")
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name, logged_in=current_user.is_authenticated)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/download/<path:filename>")
@login_required
def download(filename):
    return send_from_directory(directory="static/files", filename=filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
