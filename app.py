from flask import Flask, jsonify, render_template, request
import json
import os

app = Flask(__name__)

# Files for communication
STATE_FILE = "system_state.json"      # Read from here (Data)
CONTROL_FILE = "control_config.json"  # Write to here (Commands)

# Ensure control file exists with default mode
if not os.path.exists(CONTROL_FILE):
    with open(CONTROL_FILE, "w") as f:
        json.dump({"mode": "AUTO"}, f)

# -------------------------
# 1️⃣ PAGE ROUTES
# -------------------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/control")
def control():
    return render_template("control.html")

@app.route("/about")
def about():
    return render_template("about.html")

# -------------------------
# 2️⃣ API: READ DATA (For Dashboard)
# -------------------------
@app.route("/get-latest-data", methods=["GET"])
def get_latest_data():
    """Reads the latest sensor data written by the monitor script."""
    try:
        if not os.path.exists(STATE_FILE):
            # Return a waiting status if file doesn't exist yet
            return jsonify({"status": "waiting", "probable_source": "None"}), 202
            
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return jsonify(data)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------
# 3️⃣ API: SET MODE (For Control Panel)
# -------------------------
@app.route("/set-mode", methods=["POST"])
def set_mode():
    """Writes the desired mode to a file so the monitor script can see it."""
    try:
        mode = request.json.get("mode", "AUTO")
        
        # Write to control file
        with open(CONTROL_FILE, "w") as f:
            json.dump({"mode": mode}, f)
            
        print(f"🎛️ Control: Mode set to {mode}")
        return jsonify({"status": "success", "mode": mode})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)