from flask import Flask
from flask import render_template
import csv
import json



server = Flask(__name__)
PORT = 8080

@server.route("/")
def index():
	csv_file = open('./assets/nightingale.csv', encoding='utf-8-sig')
	reader = csv.reader(csv_file, delimiter=',')
	data = []
	for row in reader:
		datapoint = {
			'month': row[0],
			'avg_army_size': row[1],
			'zymotic_deaths': row[2],
			'injury_deaths': row[3],
			'other_deaths': row[4]
		}
		data.append(datapoint)
	return render_template('./index.html', data=json.dumps(data))

if __name__ == "__main__":
    server.run(port=PORT)