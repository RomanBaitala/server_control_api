from ..config.ext import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(240), nullable=False)

    servers = db.relationship("Server", back_populates="owner", cascade="all, delete-orphan")
