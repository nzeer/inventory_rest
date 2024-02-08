from flask import Flask, request, jsonify
from libdata import *

import csv

HOSTS_CSV = "./csv/hosts.csv"
DICT_HOSTS = {}

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "home"
    #data = request.get_json()
    #return jsonify(data), 200   

@app.route('/api/v1/get-inventory-host/<host>', methods=['GET'])
def get_inventory_host(host):
    req_host = request.args.get('listing')
    if req_host:
        if req_host == "all":
            return jsonify(DICT_HOSTS), 200     
    if host in DICT_HOSTS:
        return jsonify(DICT_HOSTS[host]), 200
 

if __name__ == "__main__":
    DICT_HOSTS = load_hosts_csv(HOSTS_CSV)
    app.run(host='0.0.0.0', port=5000, debug=True)