import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '9963dda1232a7ac15d81b9278705c95e3928d69e4acd7d7c87051c4eda76182a'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False