# My Top 10 Movies

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, URL
import requests

import config

TOP_LIMIT = 10
SECRET_KEY = "ThisIsASecretKey"
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_INFO_URL = "https://api.themoviedb.org/3/movie"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.secret_key = SECRET_KEY
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top_movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    # allow NULL ranking when creating a new entry, since it will be generated automatically
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"<Movie: {self.title} ({self.year})>"


class AddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    rating = FloatField("Rating", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')


class AddFromTMDBForm(FlaskForm):
    title = StringField("Add Movie From TMDB", validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    rating = FloatField("Your Rating (out of 10, e.g. 8.5)", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()


def parse_rating(raw_rating):
    """Convert raw rating value to float; return 0.0 when invalid."""
    try:
        rating = float(raw_rating)
    except (ValueError, TypeError):
        return 0.0
    return round(rating, 1)


def update_rankings(movies):
    """Update ranking values based on sorted movie list order."""
    rankings_updated = False
    for index, movie in enumerate(movies):
        ranking = len(movies) - index
        if movie.ranking != ranking:
            movie.ranking = ranking
            rankings_updated = True
    if rankings_updated:
        db.session.commit()


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating.desc()).limit(TOP_LIMIT).all()
    update_rankings(all_movies)
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    form = EditForm()
    movie_id = request.args.get("id", type=int)
    movie = db.session.get(Movie, movie_id) if movie_id is not None else None
    if movie is not None and form.validate_on_submit():
        movie.rating = parse_rating(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, movie=movie)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddForm()
    if form.validate_on_submit():
        new_movie = Movie(
            title=form.title.data,
            year=form.year.data,
            description=form.description.data,
            rating=parse_rating(form.rating.data),
            ranking=None,
            review=form.review.data,
            img_url=form.img_url.data
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id", type=int)
    movie = db.session.get(Movie, movie_id) if movie_id is not None else None
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/find", methods=["GET", "POST"])
def find_movie():
    form = AddFromTMDBForm()
    if form.validate_on_submit():
        params = {
            "api_key": config.TMDB_API_KEY,
            "query": form.title.data
        }
        response = requests.get(url=TMDB_SEARCH_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()["results"]
        return render_template("select.html", options=data)
    return render_template("find.html", form=form)


@app.route("/tmdb")
def add_movie_from_tmdb():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        url = f"{TMDB_INFO_URL}/{movie_api_id}"
        params = {
            "api_key": config.TMDB_API_KEY,
            "language": "en-US"
        }
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=int(data["release_date"].split("-")[0]),
            description=data["overview"],
            rating=0,
            ranking=None,
            review="",
            img_url=f"{TMDB_IMAGE_URL}{data['poster_path']}"
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("edit_rating", id=new_movie.id))
    return redirect(url_for("find_movie"))


if __name__ == "__main__":
    app.run(debug=True)
