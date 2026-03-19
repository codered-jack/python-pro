# Coffee & Wi-Fi

from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap

from cafe_data import CafeManager

SECRET_KEY = "ThisIsASecretKey"

app = Flask(__name__)
app.secret_key = SECRET_KEY
Bootstrap(app)


class CafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    location = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    time_open = StringField("Opening Time e.g. 8:00 AM", validators=[DataRequired()])
    time_close = StringField("Closing Time e.g. 5:30 PM", validators=[DataRequired()])
    coffee = SelectField("Coffee Rating", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                         validators=[DataRequired()])
    wifi = SelectField("Wifi Strength Rating", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
                       validators=[DataRequired()])
    power = SelectField("Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


# using an object to handle all the CSV stuff
cafe_list = CafeManager()


def form_to_entry(form: CafeForm):
    """Convert validated form fields to CSV row order.

    Example output:
    ["Star Cafe", "https://maps.google...", "8:00 AM", "5:30 PM", "☕☕☕", "💪💪", "🔌🔌"]
    """
    return [
        form.name.data,
        form.location.data,
        form.time_open.data,
        form.time_close.data,
        form.coffee.data,
        form.wifi.data,
        form.power.data,
    ]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = form_to_entry(form)
        cafe_list.add_cafe(new_cafe)
        return redirect("/cafes")
    return render_template("add.html", add_cafe_form=form)


@app.route("/cafes")
def cafes():
    header, entries = cafe_list.get_cafes()
    return render_template("cafes.html", header=header, cafes=entries)


if __name__ == "__main__":
    app.run(debug=True)
