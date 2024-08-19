

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy to use the SQLite database named 'SHIVANI'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?dsn=shivani.rana'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Create the table in the database
# with app.app_context():
#     db.create_all()

# Insert data into the User table
with app.app_context():
    # Create instances of the User model
    user1 = User(username='john_doe', email='john@example.com')
    user2 = User(username='jane_doe', email='jane@example.com')

    # Add the instances to the SQLAlchemy session
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes to persist the data in the database
    db.session.commit()
if __name__ == '__main__':
    app.run(debug=True)
