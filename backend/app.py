from flask import Flask, send_from_directory, request, jsonify
from config import Config
from routes.prediction_routes import prediction_bp
from auth_routes import auth_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp)
app.register_blueprint(prediction_bp)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/", methods=["GET"])
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>", methods=["GET"])
def frontend(filename):
    return send_from_directory(FRONTEND_DIR, filename)


if __name__ == "__main__":
    print("\n========== REGISTERED ROUTES ==========")

    for rule in app.url_map.iter_rules():
        print(rule, "->", rule.endpoint)

    print("=======================================\n")

    app.run(debug=True)
