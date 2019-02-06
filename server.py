from flask import Flask
from flask import render_template
import csv



server = Flask(__name__)
PORT = 8080

@server.route("/")
def index():
	csv_file = open('./assets/nightingale.csv')
	reader = csv.reader(csv_file, delimiter=',')
	data = []
	for row in reader:
		data.append(row)
	return render_template('./index.html', data=data)

if __name__ == "__main__":
    server.run(port=PORT)
