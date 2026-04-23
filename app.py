from flask import Flask

app = Flask(__name__)
app.secret_key = "campus_secret_key"

from auth import *
from booking import *
from admin import *

if __name__ == "__main__":
    app.run(debug=True)