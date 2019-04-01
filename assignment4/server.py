from flask import Flask
from flask import render_template
import csv
import json

server = Flask(__name__)
PORT = 8080

@server.route("/")
def index():
	return render_template('./index.html')

if __name__ == "__main__":
    server.run(port=PORT)
