from flask import Flask, request, jsonify
import csv
from datetime import datetime
import socket
app = Flask(__name__)

data_buffer = []
BATCH_size = 10

@app.route('/data', methods=['POST'])
def receive_data():
    global data_buffer
    
    data = request.json
    data_buffer.append(data)

    #Buffer
    if len(data_buffer) >= BATCH_size:
        save_to_csv(data_buffer)
        data_buffer.clear()
    
    return jsonify(success = True), 200

def save_to_csv(buffered_data):
    filename = datetime.now().strftime('%d%H%M%S') + ".csv"

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = buffered_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in buffered_data:
            writer.writerow(data)

if __name__ == '__main__':
    app.run(host = socket.gethostname(), port = 9000, debug = True)
    