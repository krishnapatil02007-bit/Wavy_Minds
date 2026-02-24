from flask import Flask, jsonify, render_template, request
import json
import os

app = Flask(__name__)


STATE_FILE = "system_state.json"      
CONTROL_FILE = "control_config.json"  


if not os.path.exists(CONTROL_FILE):
    with open(CONTROL_FILE, "w") as f:
        json.dump({"mode": "AUTO"}, f)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/control")
def control():
    return render_template("control.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/get-latest-data", methods=["GET"])
def get_latest_data():
    """Reads the latest sensor data written by the monitor script."""
    try:
        if not os.path.exists(STATE_FILE):

            return jsonify({"status": "waiting", "probable_source": "None"}), 202
            
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return jsonify(data)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/set-mode", methods=["POST"])
def set_mode():
    """Writes the desired mode to a file so the monitor script can see it."""
    try:
        mode = request.json.get("mode", "AUTO")
        

        with open(CONTROL_FILE, "w") as f:
            json.dump({"mode": mode}, f)
            
        print(f"🎛️ Control: Mode set to {mode}")
        return jsonify({"status": "success", "mode": mode})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
