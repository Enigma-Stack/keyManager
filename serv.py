from flask import Flask, jsonify, request
import random
import threading
import json
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Read key-UUID pairs from JSON file
def load_key_uuid_pairs(filename):
    with open(filename, 'r') as file:
        return json.load(file)

key_uuid_pairs = load_key_uuid_pairs('keys.json')

lock = threading.Lock()

@app.route('/genotpkey', methods=['GET'])
def genotpkey():
    length = request.args.get('length', type=int, default=32)
    # Calculate the number of keys needed
    num_keys_needed = length // 32 + (1 if length % 32 else 0)

    with lock:
        if num_keys_needed > len(key_uuid_pairs):
            return jsonify({"error": "Not enough keys available"}), 404

        selected_pairs = random.sample(list(key_uuid_pairs.items()), num_keys_needed)
        return jsonify(selected_pairs)

@app.route('/getotpkey', methods=['POST'])
def getotpkey():
    data = request.get_json()
    uuids = data.get('uuids', [])
    keys = []
    with lock:
        for uuid_value in uuids:
            print(uuid_value)
            for uuid, key in list(key_uuid_pairs.items()):
                if uuid == uuid_value:
                    keys.append(key)
                    print(keys)
                    del key_uuid_pairs[uuid]
                    break
    return jsonify(keys)


# @app.route('/getaeskey', methods=['GET'])
# def getaeskey():
#     input_uuid = request.args.get('uuid')
#     with lock:
#         if input_uuid:
#             for key, uuid_value in list(key_uuid_pairs.items()):
#                 if uuid_value == input_uuid:
#                     del key_uuid_pairs[key]
#                     return jsonify({"key": key})
#             return jsonify({"error": "UUID not found"}), 404
#         else:
#             if not key_uuid_pairs:
#                 return jsonify({"error": "No more pairs available"}), 404
#             key, uuid_value = random.choice(list(key_uuid_pairs.items()))
#             return jsonify({"key": key, "uuid": uuid_value})

# @app.route('/genaeskey', methods=['GET'])
# def genaeskey():
#     with lock:
#         if not key_uuid_pairs:
#             return jsonify({"error": "No more pairs available"}), 404
        
#         key, uuid_value = random.choice(list(key_uuid_pairs.items()))
#         return jsonify({"key": key, "uuid": uuid_value})

if __name__ == '__main__':
    app.run(debug=True)
