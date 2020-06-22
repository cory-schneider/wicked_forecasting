from datetime import datetime
from forecastapp import db
from flask import current_app

class PdcnPair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pdcnMain = db.Column(db.String(7), nullable=False)
    pdcnAlt = db.Column(db.String(7), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"PDCNPair('{self.pdcnMain}', '{self.pdcnAlt}')"

class WholesalerFamily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    nums = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"WholesalerPair('{self.wslrName}', '{self.wslrNum}')"
