from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///influencer_sponsor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    profile_pic = db.Column(db.String(200))

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print("Admin user already exists!")
            return

        # Create new admin user
        password = "admin123"  # You can change this
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        admin_user = User(
            username="admin",
            password=hashed_password,
            email="admin@example.com",
            role="admin",
            is_active=True
        )

        db.session.add(admin_user)
        db.session.commit()

        print("\nAdmin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@example.com")

if __name__ == "__main__":
    create_admin()