from flask import Flask

app = Flask(__name__)

app.secret_key = "1490"

from flask_app.controllers.user import *