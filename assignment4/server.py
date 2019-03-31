from flask import Flask
from flask import render_template
import csv
import json



server = Flask(__name__)
PORT = 8080

@server.route("/")
def index():
	nightingale_csv = open('./assets/nightingale.csv', encoding='utf-8-sig')
	reader = csv.reader(nightingale_csv, delimiter=',')
	nightingale_data = []
	for row in reader:
		datapoint = {
			'month': row[0],
			'avg_army_size': row[1],
			'zymotic_deaths': row[2],
			'injury_deaths': row[3],
			'other_deaths': row[4]
		}
		nightingale_data.append(datapoint)
	
	minard_csv = open('./assets/minard.csv', encoding='utf-8-sig')
	reader = csv.reader(minard_csv, delimiter=',')
	minard_data = {
		"cities": [],
		"temps": [],
		"army": []
	}

	for row in reader:
		city_coord = row[0] and row[1] and row[2]
		temp_coord = row[3] and row[4] and row[5] and row[6] and row[7]
		army_coord = row[8] and row[9] and row[10] and row[11] and row[12]

		if city_coord:
			minard_data["cities"].append({
				"longitude": row[0],
				"latitude": row[1],
				"city_name": row[2]
			})
		if temp_coord:
			minard_data["temps"].append({
				"longitude": row[3],
				"temp": row[4],
				"days": row[5],
				"month": row[6],
				"day_of_month": row[7]
			})
		if army_coord:
			minard_data["army"].append({
				"longitude": row[8],
				"latitude": row[9],
				"survivors": row[10],
				"direction": row[11],
				"division": row[12]
			})

	return render_template('./index.html', nightingale_data=json.dumps(nightingale_data), minard_data=json.dumps(minard_data))

if __name__ == "__main__":
    server.run(port=PORT)
