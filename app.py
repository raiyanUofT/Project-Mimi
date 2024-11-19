from flask import Flask, render_template
from database import db
from pantry.routes import pantry_blueprint
import os
from config import DevelopmentConfig, ProductionConfig
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration dynamically based on environment
if os.getenv('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

# Initialize the `db` object with the Flask app
db.init_app(app)

# Register the pantry blueprint
app.register_blueprint(pantry_blueprint, url_prefix='/pantry')

# Serve frontend with dynamic API URL
@app.route('/')
def serve_frontend():
    api_url = os.getenv('API_URL', 'http://127.0.0.1:5000/pantry')  # Default for local development
    return render_template('index.html', api_url=api_url)

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], host="0.0.0.0")
