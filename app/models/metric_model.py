from ..config.ext import db
from datetime import datetime, timezone

class Metric(db.Model):
    __tablename__ = 'metrics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    cpu_usage = db.Column(db.Float, nullable=False)
    cpu_temperature = db.Column(db.Float, nullable=False)
    memory_usage = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    server = db.relationship("Server", backref=db.backref("metrics", lazy=True))

    __table_args__ = (
        db.UniqueConstraint('server_id', 'timestamp', name='_server_timestamp_uc'),
    )