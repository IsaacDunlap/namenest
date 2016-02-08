#!/usr/bin/env python
#
# Create an app and set up the command line arguments to run the app as
# a command line program.

import os

from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models import User, Role

# Configure the application and set up migration and command line
# management objects.
app = create_app(os.getenv('NAMEBASE_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def test():
    """Run the unit tests."""
    # Run the unit tests.
    #
    # Raises: ???

    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


def make_shell_context():
    # Provide a dictionary of shell commands that extend application
    # functionality.
    #
    # Returns:
    #   (dictionary) - supplies keyword arguments for the shell context.

    return {
        app: app,
        db: db,
        User: User,
        Role: Role,
    }


# Add commands to the command line application.
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
