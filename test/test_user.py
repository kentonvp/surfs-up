import unittest
from surfsup.user import Activity, AbilityLevel, AccessLevel, ActivityPreferences, ShortboardPreferences, User

class TestUser(unittest.TestCase):

    def test_user_serialization(self):
        user = User(
            'Foobar',
            Activity.SHORTBOARD,
            { Activity.SHORTBOARD: ShortboardPreferences() }
        )
        self.assertEqual(user, User.de_json(user.to_dict()))
