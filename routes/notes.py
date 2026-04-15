from app import app
from extensions import db
from models import User, Note
from faker import Faker

fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(username="test1")
    user1.set_password("1234")

    user2 = User(username="test2")
    user2.set_password("1234")

    db.session.add_all([user1, user2])
    db.session.commit()

    for user in [user1, user2]:
        for _ in range(5):
            note = Note(
                title=fake.word(),
                content=fake.text(),
                user_id=user.id
            )
            db.session.add(note)

    db.session.commit()

    print("Seeded successfully!")