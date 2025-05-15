from flask import Flask, request, jsonify

app = Flask(__name__)

switch_states = {str(i): "OFF" for i in range(1, 9)}
valid_devices = {"esp32_001": True}

@app.route("/switch/<switch_id>", methods=["GET", "POST"])
def switch(switch_id):
    if switch_id not in switch_states:
        return jsonify({"error": "Invalid switch"}), 404
    if request.method == "GET":
        return jsonify({"state": switch_states[switch_id]})
    if request.method == "POST":
        data = request.json
        new_state = data.get("state", "OFF")
        if new_state not in ["ON", "OFF"]:
            return jsonify({"error": "Invalid state"}), 400
        switch_states[switch_id] = new_state
        return jsonify({"message": f"Switch {switch_id} set to {new_state}"}), 200

@app.route("/auth/<device_id>", methods=["GET"])
def auth(device_id):
    if valid_devices.get(device_id):
        return jsonify({"auth": "ok"})
    return jsonify({"auth": "denied"}), 403

@app.route("/")
def home():
    return "IoT Backend is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
