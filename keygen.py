import os
import uuid
import json

def generate_hex_key():
    # Generate a random hexadecimal key of 256 bits
    key = os.urandom(32)  # 32 bytes for a 256-bit key
    hex_key = key.hex()   # Convert bytes to hexadecimal
    return hex_key

def create_json_file_with_keys(filename):
    keys_dict = {}

    for _ in range(50000):
        unique_id = str(uuid.uuid4())
        hex_key = generate_hex_key()
        keys_dict[unique_id] = hex_key

    with open(filename, 'w') as json_file:
        json.dump(keys_dict, json_file, indent=4)

# Usage
create_json_file_with_keys("keys.json")
