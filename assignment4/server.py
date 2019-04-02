from flask import Flask, render_template, request, Response
import csv
import json

server = Flask(__name__)
PORT = 8080
FPS = 30

def evaluate_ccr(data):
    """ Evaluate CCR through every datapoint, and dump the CCR for that datapoint. """
    ccr_data = []
    compressions = 0
    prev_compression_time = None
    interrupted_frames = 0

    for index, datapoint in enumerate(data):
        elapsed_time = float(index / FPS)
        if datapoint[1] == "Compression":
            compressions += 1
            if prev_compression_time:
                time_diff = elapsed_time - prev_compression_time
                ccr = 60 / time_diff
                ccr_data.append(ccr)
            else:
                ccr_data.append(None)
            prev_compression_time = elapsed_time
        else:
            interrupted_frames += 1
            ccr_data.append(None)
    return ccr_data

@server.route("/")
def index():
	dataset_name = request.args.get('dataset')
	if not dataset_name:
		dataset_name = 'ideal'
	gt_csv = open('./assets/gt_%s.csv' % dataset_name, encoding='utf-8-sig')
	results_csv = open('./assets/results_%s.csv' % dataset_name, encoding='utf-8-sig')
	gt_data = []
	results_data = []

	reader = csv.reader(gt_csv, delimiter=',')
	for row in reader:
		gt_data.append((float(row[1]) if row[1] != '-' else None, row[3] if row[3] != 'None' else None))

	reader = csv.reader(results_csv, delimiter=',')
	for row in reader:
		results_data.append((float(row[4]), row[3] if row[3] != 'None' else None))

	gt_ccr = evaluate_ccr(gt_data)
	results_ccr = evaluate_ccr(results_data)

	return render_template('./index.html', gt_data=json.dumps(gt_data), results_data=json.dumps(results_data), gt_ccr=json.dumps(gt_ccr), results_ccr=json.dumps(results_ccr), fps=FPS, dataset=dataset_name.capitalize())

@server.route("/assets/<file_name>", methods=["GET"])
def get_file(file_name):
	return server.send_static_file('./assets/%s' % file_name)

if __name__ == "__main__":
    server.run(debug=True, port=PORT)
