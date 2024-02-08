from flask import Flask, request, jsonify
import csv

HOSTS_CSV = "./csv/pop_hosts.csv"
DICT_HOSTS = {}

with open(HOSTS_CSV, newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
    for row in spamreader:
        host_name, list_ip, list_os_info = eval(", ".join(row))
        DICT_HOSTS[host_name] = {"ip": list_ip, "os": list_os_info} 
        #print(", ".join(row))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "home"
    #data = request.get_json()
    #return jsonify(data), 200   

@app.route('/api/v1/get-inventory-host/<host>', methods=['GET'])
def get_inventory_host(host):
    if host in DICT_HOSTS:
        return jsonify(DICT_HOSTS[host]), 200
    '''host = {"host": "uhhy-whatever-1",
            "ip":   "10.1.1.244",
            "os":   "Ubuntu",
            "version": "20"
            }
    req_id = request.args.get('vscodeBrowserReqId')
    if req_id:
        host['vscodeBrowserReqId'] = req_id
    #return "get_inventory"
    #data = request.get_json()
    return jsonify(host), 200'''



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)