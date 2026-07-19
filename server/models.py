from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        allowed = ['strength', 'cardio', 'flexibility', 'balance']
        if value not in allowed:
            raise ValueError(f"Category must be one of {allowed}.")
        return value

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'