# __init__.py
# 2018-08-15 david.montaner@gmail.com
# fds-tools templates.

import os

templates_dir = os.path.abspath(os.path.dirname(__file__))

templates = os.listdir(templates_dir)
templates = [x for x in templates if 'fds-template' in x]
templates = [os.path.join(templates_dir, x) for x in templates]

# print(templates_dir)
# print(templates)
