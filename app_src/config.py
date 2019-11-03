import os
import json
import logging

try:
    with open(os.path.dirname(os.path.abspath(__file__)) + '/config.json') as events_file:
        config = json.load(events_file)
except:
    logging.exception('unable to read config.json')
