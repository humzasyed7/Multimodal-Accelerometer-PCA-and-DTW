import csv
import socket
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
buffer = []

@app.route('/data', methods=['POST'])
def receive_data():
    global buffer
    
    jsonData = request.json
    buffer.append(jsonData)

    # When the buffer exceeds 10, write data to csv and clear the buffer. Repeat until all the data is written to the csv
    if len(buffer) >= 10:
        save_to_csv(buffer)
        buffer.clear()
    return jsonify(success = True), 200

def save_to_csv(buffer_subset):
    path = datetime.now().strftime('%d%H%M%S') + ".csv" #Set =the file name based on the timestamp

    with open(path, 'w', newline='') as csvfile:
        headers = buffer_subset[0].keys() # Use the keys from the jsonData as the headers
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        # Write each row of the buffer_subset (10 json Data Points) into the csv
        for row_data in buffer_subset:
            writer.writerow(row_data)

# Run the app! This will make the server go live and allow data to be sent from the Phone via SensLogger
if __name__ == '__main__':
    app.run(host = socket.gethostname(), port = 9000, debug = True)
    