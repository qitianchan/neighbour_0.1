# -*- coding: utf-8 -*-
#!/usr/bin/env python
import time

from flask_script import (Manager, Shell, Server, prompt, prompt_pass,
                          prompt_bool)


from neighbour.app import create_app

# Use the development configuration if available
from neighbour.configs.default import DefaultConfig as Config

app = create_app()
manager = Manager(app)


# Run local server
manager.add_command("runserver", Server("localhost", port=8001))


# @manager.command
# def initdb():
#     """Creates the database."""
#
#     upgrade()
#
#
# @manager.command
# def dropdb():
#     """Deletes the database."""
#
#     db.drop_all()
#

if __name__ == "__main__":
    manager.run()
