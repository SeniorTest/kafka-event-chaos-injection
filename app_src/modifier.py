# internal imports
from datetime import datetime, timedelta
import logging
import random
from collections.abc import MutableMapping
import sys
from inspect import getmembers, isfunction

# own imports
import config
import utils

logger = logging.getLogger(__name__)


def __delete_keys_from_dict(dictionary, keys):
    keys_set = set(keys)

    modified_dict = {}
    for key, value in dictionary.items():
        if key not in keys_set:
            if isinstance(value, MutableMapping):
                modified_dict[key] = __delete_keys_from_dict(value, keys_set)
            else:
                modified_dict[key] = value
    return modified_dict


def __modify_value_in_dict(dictionary, keys):
    keys_set = set(keys)

    modified_dict = {}
    for key, value in dictionary.items():
        if key not in keys_set:
            if isinstance(value, MutableMapping):
                modified_dict[key] = __modify_value_in_dict(value, keys_set)
            else:
                modified_dict[key] = value
        else:
            modified_dict[key] = 'bla'
    return modified_dict


def __modify_timestamp(dictionary, keys):
    # keys are ignored here, in order to make the function call in process_event generic
    # todo: reconsider refactoring, since ignoring parameters does not seem ok
    keys_set = ['timestamp']

    modified_dict = {}
    for key, value in dictionary.items():
        if key not in keys_set:
            if isinstance(value, MutableMapping):
                modified_dict[key] = __modify_value_in_dict(value, keys_set)
            else:
                modified_dict[key] = value
        else:
            logging.debug('changing timestamp from')
            logging.debug(value)
            value_as_datetime = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
            modified_timestamp = value_as_datetime + timedelta(days=random.randint(-365, 365))
            modified_dict[key] = modified_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            logging.debug(modified_dict[key])
    return modified_dict


def process_event(event):
    logger.debug('processing event ')
    logger.debug(event)

    inject_fault = True if random.randint(0, 100) <= int(config.config['fault_injection_rate_in_percent']) else False

    if inject_fault:
        # get all private methods from modifier (this module) module
        current_module = sys.modules[__name__]
        dict_of_fault_injection_types = dict(
            [o for o in getmembers(current_module) if isfunction(o[1]) and o[0].startswith('__')])

        selected_injection_type = random.choice(list(dict_of_fault_injection_types.keys()))
        logger.info('selected injection type: ' + selected_injection_type)

        possible_fields_for_modification = utils.get_all_keys(event)
        logger.debug('possible keys for modification: ')
        logger.debug(possible_fields_for_modification)

        key_value_to_modify = random.choice(possible_fields_for_modification)

        # calling function based on the selected injection type
        event = dict_of_fault_injection_types[selected_injection_type](event, [key_value_to_modify])

        logger.info('run ' + selected_injection_type + ' on ' + key_value_to_modify)

    else:
        logger.info('did not modify event')

    logger.debug('remaining event:')
    logger.debug(event)

    return event
