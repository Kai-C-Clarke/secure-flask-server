from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import ssl
import os
import json

app = Flask(__name__)

# Hardcoded credentials for simplicity (replace with secure storage later)
users = {
    "kai": generate_password_hash("changeme")
}

# File paths for inbox and outbox storage
inbox_file = "inbox.json"
outbox_file = "outbox.json"

# Basic Auth Decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_password_hash(users.get(auth.username, ""), auth.password):
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

# Inbox Route - stores JSON to file
@app.route('/kai/inbox', methods=['POST'])
@requires_auth
def inbox():
    data = request.get_json()
    # Write data to inbox.json and outbox.json
    with open(inbox_file, 'w') as f:
        json.dump(data, f, indent=4)
    with open(outbox_file, 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({"status": "received", "data": data}), 200

# Outbox Route - retrieves JSON from file
@app.route('/kai/outbox', methods=['GET'])
@requires_auth
def outbox():
    if not os.path.exists(outbox_file):
        return jsonify({"status": "empty"})
    with open(outbox_file, 'r') as f:
        data = json.load(f)
    return jsonify(data), 200

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=5000, ssl_context=context)
