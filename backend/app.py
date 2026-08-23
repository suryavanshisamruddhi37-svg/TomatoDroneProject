from flask import Flask
from config import Config
from routes.prediction_routes import prediction_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(prediction_bp)

@app.route('/')
def home():
    return {
    "message": "CropCare Backend is running",
    "status": "success"
    }

@app.route('/api/health')
def heath():
    return{
        "status": "healthy",
    }

if __name__ == '__main__':
    app.run(debug=True,)