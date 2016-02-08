# Contains basic tests of the application and the various application
# models.
#
# Classes:
#   BasicTestCase - Methods for setting up a test application and
#                   sanity checking the test application.
#   UserModelTestCase - Methods for testing the user model's
#                       basic functionality.

import unittest

from flask import current_app

from app import create_app, db
from app.models import User


class BasicTestCase(unittest.TestCase):
    # A set of tests for sanity checking a testing application.
    #
    # Inherits from the unittest TestCase class.
    #
    # Methods:
    #   ---------- PUBLIC ----------
    #   setUp (override) - sets up the testing application and creates
    #                      all tables in the database.
    #   tearDown (override) - deletes the database tables and the
    #                         application context.
    #   test_app_exists - checks that the current app exists.
    #   test_app_is_testings - checks that the app is configured for
    #                          testing.
    #
    # Attributes:
    #   ---------- PUBLIC ----------
    #   app (Flask) - the test application for unit testing.
    #   app_context (AppContext) - the context of the test application.

    def setUp(self):
        # Creates a testing application, and push the corresponding
        # application context. Create all tables in the test database.

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Wipes the testing database and remove the test application
        # context.

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        # Checks that the current application has been successfully
        # created.
        #
        # Raises:
        #   failureException  - when the current application is None.

        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        # Checks that the current application is in the testing
        # configuration.
        #
        # Raises:
        #   failureException - if the current application is a non-
        #                      testing application.

        self.assertTrue(current_app.config['TESTING'])


class UserModelTestCase(unittest.TestCase):
    # Tests the password hashing functionality of the User model.
    #
    # Inherits from the unittest TestCase class.
    #
    # Methods:
    #   ---------- PUBLIC ----------
    #   test_password_setter - checks that the password hash is stored.
    #   test_no_password_getter - checks that the password attribute of
    #                             the User model is write-only.
    #   test_password_verification -
    #       checks that password verification against hashes works.
    #   test_password_salts_are_random -
    #       checks that two users with the same password have different
    #       password hashes.

    def test_password_setter(self):
        # Checks that a password hash is stored when a User's
        # password attribute is set.
        #
        # Raises:
        #   failureException - when the password_hash attribute of the
        #                      User instance is None.

        user = User(password='flaskisawesome')
        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        # Checks that the password attribute of a User instance is
        # write-only.
        #
        # Raises:
        #   AssertionError -
        #       when no error is raised when trying to get the password
        #       attribute. If an error (other than an AssertionError)
        #       is raised whilst trying to get the password, then that
        #       error isn't caught.

        user = User(password='flaskisawesome')
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        # Checks that a password can be verified against a User
        # instance's password_hash attribute, and doesn't incorrectly
        # verify a wrong password.
        #
        # Raises:
        #   failureException - when either a correct password fails to
        #                      be verified, or a wrong password is
        #                      verified.

        user = User(password='flaskisawesome')
        self.assertTrue(user.verify_password('flaskisawesome'))
        self.assertFalse(user.verify_password('flaskisnotawesome'))

    def test_password_salts_are_random(self):
        # Checks that two users with the same password have different
        # password hashes.
        #
        # Raises:
        # failureException - when the password hashes of the two users
        #                    are equal.

        pass
        user1 = User(password='flaskisawesome')
        user2 = User(password='flaskisawesome')
        self.assertTrue(user1.password_hash != user2.password_hash)
