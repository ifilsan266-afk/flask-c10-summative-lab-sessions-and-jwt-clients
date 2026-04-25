from app import create_app
from models import db, User, Note
from faker import Faker

fake = Faker()
app = create_app()

with app.app_context():
    # Clear existing data
    Note.query.delete()
    User.query.delete()
    db.session.commit()

    # Create users
    user1 = User(username="filsan")
    user1.password_hash = "password123"

    user2 = User(username="trainer_jane")
    user2.password_hash = "password123"

    user3 = User(username="john_doe")
    user3.password_hash = "password123"

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Create notes for each user
    categories = ["general", "work", "personal", "health", "finance"]

    for user in [user1, user2, user3]:
        for i in range(5):
            note = Note(
                title=fake.sentence(nb_words=4),
                content=fake.paragraph(nb_sentences=3),
                category=categories[i % len(categories)],
                user_id=user.id
            )
            db.session.add(note)

    db.session.commit()
    print("Database seeded successfully!")
    print(f"Users: {User.query.count()}")
    print(f"Notes: {Note.query.count()}")
