from flask import Flask, flash, request, redirect, url_for, render_template
import os
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics

from src.database import db, create_database
from src.models import Predictions
from src.weather_api_provider import WeatherProvider, WeatherAPIError

app = Flask(__name__)
metrics = PrometheusMetrics(app)

basedir = os.path.abspath(os.path.join(app.root_path, '..'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db', 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.cli.command('initialize-database')
def initialize_database():
    create_database(app)

@app.route("/")
@metrics.counter("requests_index_total", "Number of requests to index")
def index():
    predictions = Predictions.query.order_by(Predictions.day.desc()).all()
    return render_template('index.html', predictions=predictions)

@app.route("/health")
@metrics.do_not_track()
def health():
    pass

@app.route("/predict", methods=["POST"])
def predict():
    lat = request.form.get("lat", "")
    lon = request.form.get("lon", "")

    if not lat or not lon:
        flash("Invalid latitude or longitude entered")
        return redirect(url_for("index"), "danger")

    try:
        provider = WeatherProvider()
        predictions = provider.prediction_for(float(lat), float(lon))

        for day, prediction in predictions.items():
            row = Predictions(
                    lat=lat,
                    lon=lon,
                    day=datetime.strptime(day, "%Y-%m-%d"),
                    min_temperature=prediction["min"],
                    mean_temperature=prediction["mean"],
                    max_temperature=prediction["max"]
            )
            db.session.add(row)
        db.session.commit()
        flash("New predictions added", "success")
        return redirect(url_for("index"))

    except WeatherAPIError as err:
        flash(str(err), "danger")
        return redirect(url_for("index"))
    except ValueError:
        flash("Could not parse latitude or longitude. Make sure your entered values follow floating point convention", "danger")
        return redirect(url_for("index"))
