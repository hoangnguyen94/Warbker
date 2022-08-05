"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py



import os

from unittest import TestCase

from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables( we do this here, so we only create tables
# once for all tests) we will create new test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test view for message"""

    def setUp(self):
        """Create test client and sample data"""
        db.drop_all()
        db.create_all()

        self.uid = 99999
        u = User.signup("testing", "testing@test.test","password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):
        """Does model work?"""

        m = Message(
            text="a message",
            user_id = self.uid
        )

        db.session.add(m)
        db.session.commit()

        #User should have 1 message
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "a message")

    def test_message_likes(self):
        m1 = Message(
            text="a message",
            user_id=self.uid
        )

        m2 = Message(
            text="world of message",
            user_id=self.uid
        )

        u = User.signup("secondtest", "test@test.test", "password", None)
        uid = 88888
        u.id = uid
        db.session.add_all([m1, m2, u])

        u.likes.append(m1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, m1.id)


