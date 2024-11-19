from app import app
from database import db

def create_tables():
    """Initialize the database and create all tables."""
    with app.app_context():
        db.create_all()
        print(f"Database initialized: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == "__main__":
    create_tables()
