import BAC0,time,json 
from flask import Flask, request, jsonify
import flask
import logging


logging.basicConfig(filename='flask_app_log.log', level=logging.WARNING)



#STATIC_BACNET_IP = '192.168.0.103/24'
#bacnet = BAC0.lite(IP=STATIC_BACNET_IP)

bacnet = BAC0.lite()


#scan network
time.sleep(1)
devices = bacnet.whois(global_broadcast=True)
device_mapping = {}
for device in devices:
    if isinstance(device, tuple):
        device_mapping[device[1]] = device[0]
        logging.warning("Detected device %s with address %s" % (str(device[1]), str(device[0])))
print(device_mapping)
print((str(len(device_mapping)) + " devices discovered on network."))


#start flask app
app = Flask(__name__)



#READ
@app.route('/bacnet/read/single', methods=['GET'])
def reader():

    try:
        json_data = flask.request.json
        address = json_data["address"]
        object_type = json_data["object_type"]
        object_instance = json_data["object_instance"]

        read_vals = f'{address} {object_type} {object_instance} presentValue'
        print("Excecuting read_vals statement:", read_vals)
        read_result = bacnet.read(read_vals)
        read_result_round = round(read_result,2)
        response_obj = { 'status' : 'success', 'info' : read_result_round }
        
    except Exception as error:
        logging.error("Error trying BACnet Read {}".format(error))
        info = str(error)
        response_obj = { 'status' : 'fail', 'info' : info }
        return json.dumps(response_obj), 500

    return json.dumps(response_obj)


#WRITE
@app.route('/bacnet/write/single', methods=['GET'])
def writer():

    try:
        json_data = flask.request.json
        address = json_data["address"]
        object_type = json_data["object_type"]
        object_instance = json_data["object_instance"]
        value = json_data["value"]
        priority = json_data["priority"]
    
        write_vals = f'{address} {object_type} {object_instance} presentValue {value} - {priority}'
        print("Excecuting write_vals statement:", write_vals)
        bacnet.write(write_vals)
        info = f'BACnet point written to device'
        response_obj = { 'status' : 'success', 'info' : info }
        
    except Exception as error:
        logging.error("Error trying BACnet Read {}".format(error))
        info = str(error)
        response_obj = { 'status' : 'fail', 'info' : info }
        return json.dumps(response_obj), 500

    return json.dumps(response_obj)


#RELEASE
@app.route('/bacnet/release/single', methods=['GET'])
def releaser():

    try:
        json_data = flask.request.json
        address = json_data["address"]
        object_type = json_data["object_type"]
        object_instance = json_data["object_instance"]
        priority = json_data["priority"]
    
        write_vals = f'{address} {object_type} {object_instance} presentValue null - {priority}'
        print("Excecuting write_vals statement:", write_vals)
        bacnet.write(write_vals)
        info = f'BACnet point release to device'
        response_obj = { 'status' : 'success', 'info' : info }
        
    except Exception as error:
        logging.error("Error trying BACnet Read {}".format(error))
        info = str(error)
        response_obj = { 'status' : 'fail', 'info' : info }
        return json.dumps(response_obj), 500

    return json.dumps(response_obj)


if __name__ == '__main__':
    print("Starting main loop")
    app.run(debug=True,port=5000,host="127.0.0.1",use_reloader=False)

