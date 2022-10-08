# -*- coding: utf-8 -*-
# Coded By Kuduxaaa

import uuid

from app import db

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(255), unique=True, nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    vin_code = db.Column(db.String(20), nullable=False)
    plate_number = db.Column(db.String(7), nullable=False)
    tech_passport_number = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    files = db.Column(db.Text, nullable=False)
    

    def __init__(self, brand, year, model, vin_code, plate_number, tech_passport_number, phone_number, files):
        self.uuid = str(uuid.uuid4())
        self.brand = brand
        self.year = year
        self.model = model
        self.vin_code = vin_code
        self.plate_number = plate_number
        self.tech_passport_number = tech_passport_number
        self.phone_number = phone_number
        self.files = files


    def save(self):
        """
        save in the database
        """

        db.session.add(self)
        db.session.commit()
        return True



    def delete(self):
        """
        delete from database
        """

        db.session.delete(self)
        db.session.commit()
        return True


    def __repr__(self):
        return '<Order %r>' % self.uuid
