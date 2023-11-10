from models import User, db, bcrypt, Feedback
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

feedback1= Feedback(title='First Post', content="This is my first post!", username = user1)
feedback2= Feedback(title='Second Post', content="Oh hi again! This is my second post!", username = user1)
feedback3=Feedback(title='Events Today?', content="Does anyone know of anything cool happening today in town?", username = user2)

