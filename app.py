from flask import Flask, send_from_directory
from database import db
import config
from pantry.routes import pantry_blueprint

app = Flask(__name__, static_folder='static')
app.config.from_object(config.Config)

# Initialize the `db` object with the Flask app
db.init_app(app)

# Register Blueprints
app.register_blueprint(pantry_blueprint, url_prefix='/pantry')

# Serve the static frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
