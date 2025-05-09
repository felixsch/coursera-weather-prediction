from src.database import db
from datetime import datetime, timezone

class Predictions(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    day = db.Column(db.Date, nullable=False) 

    min_temperature = db.Column(db.Float, nullable=True)
    mean_temperature = db.Column(db.Float, nullable=True)
    max_temperature = db.Column(db.Float, nullable=True)
