# Cafe & Wifi API

import random

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

SECRET_API_KEY = "ThisIsASecretKey"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """Return row as a serializable dictionary."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


def to_bool(raw_str):
    """Convert common truthy/falsy text values to bool.

    Examples:
    "true", "1", "yes" -> True
    "false", "0", "no", None -> False
    """
    if raw_str is None:
        return False
    value = str(raw_str).strip().lower()
    if value in {"true", "1", "yes", "y"}:
        return True
    if value in {"false", "0", "no", "n"}:
        return False
    return False


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random():
    all_cafes = Cafe.query.all()
    if not all_cafes:
        return jsonify(error={"Not Found": "No cafes found in database."}), 404
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all():
    all_cafes = Cafe.query.all()
    # using list comprehension
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search():
    if "loc" in request.args:
        location = request.args.get("loc").strip().title()
        matches = Cafe.query.filter_by(location=location).all()
        if matches:
            return jsonify(cafes=[cafe.to_dict() for cafe in matches])
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404
    return jsonify(error={"Invalid query": "No location was specified."}), 400


@app.route("/add", methods=["POST"])
def add_cafe():
    if request.headers.get("api-key") == SECRET_API_KEY:
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            seats=request.form.get("seats"),
            has_toilet=to_bool(request.form.get("toilet")),
            has_wifi=to_bool(request.form.get("wifi")),
            has_sockets=to_bool(request.form.get("sockets")),
            can_take_calls=to_bool(request.form.get("calls")),
            coffee_price=request.form.get("coffee_price")
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"Success": "Successfully added the new cafe."})
    return jsonify(error={"Unauthorized": "You are not authorized to perform this operation."}), 401


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        new_price = request.args.get("new_price")
        if not new_price:
            return jsonify(error={"Invalid query": "new_price is required."}), 400
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"Success": "Successfully updated the price."}), 200
    return jsonify(error={"Not Found": "There is no cafe with the provided id."}), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def remove_cafe(cafe_id):
    if request.headers.get("api-key") == SECRET_API_KEY:
        cafe = Cafe.query.get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"Success": "Successfully removed the cafe."}), 200
        else:
            return jsonify(error={"Not Found": "There is no cafe with the provided id."}), 404
    return jsonify(error={"Unauthorized": "You are not authorized to perform this operation."}), 401


if __name__ == "__main__":
    app.run(debug=True)
