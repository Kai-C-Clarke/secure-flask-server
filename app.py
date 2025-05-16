from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import ssl

app = Flask(__name__)

# Hardcoded credentials for simplicity (replace with secure storage later)
users = {
    "kai": generate_password_hash("changeme")
}

# Basic Auth Decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_password_hash(users.get(auth.username, ""), auth.password):
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

# Inbox Route
@app.route('/kai/inbox', methods=['POST'])
@requires_auth
def inbox():
    data = request.get_json()
    return jsonify({"received": data}), 200

# Outbox Route
@app.route('/kai/outbox', methods=['GET'])
@requires_auth
def outbox():
    dummy_message = {"message": "This is Kai's outbox placeholder."}
    return jsonify(dummy_message), 200

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=5000, ssl_context=context)
