from flask import Flask
from database import db
import config
from pantry.routes import pantry_blueprint

app = Flask(__name__)
app.config.from_object(config.Config)

# Initialize the `db` object with the Flask app
db.init_app(app)

# Register Blueprints
app.register_blueprint(pantry_blueprint, url_prefix='/pantry')

if __name__ == "__main__":
    app.run(debug=True)
