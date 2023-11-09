from models import User, db, bcrypt
from app import app

# Drop and recreate the database
db.drop_all()
db.create_all()

# Clear existing users
User.query.delete()

# Sample user data
hashed_password = bcrypt.generate_password_hash("password").decode("utf-8")

user1 = User(username='user1', password=hashed_password, email='user1@example.com', first_name='John', last_name='Doe')
user2 = User(username='user2', password=hashed_password, email='user2@example.com', first_name='Jane', last_name='Doe')
user3 = User(username='user3', password=hashed_password, email='user3@example.com', first_name='Bob', last_name='Smith')

# Add users to the session
db.session.add_all([user1, user2, user3])

# Commit the changes
db.session.commit()
