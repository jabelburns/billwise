from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route("/api/bills/<state>", methods=["GET"])
def bills(state):
    try:
        with open(f"data/{state}_bills.json", "r") as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify([]), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
