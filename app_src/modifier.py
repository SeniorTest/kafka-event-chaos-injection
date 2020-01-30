# internal imports
from datetime import datetime, timedelta
import logging
import random
from collections.abc import MutableMapping

# own imports
import config
import utils

logger = logging.getLogger(__name__)


def change_timestamp(old_timestamp):
    logging.debug('changing timestamp from')
    logging.debug(old_timestamp)
    try:
        value_as_datetime = datetime.strptime(old_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        changed_timestamp = (value_as_datetime + timedelta(days=random.randint(-365, 365))).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        logging.debug(changed_timestamp)
    except ValueError:
        logging.debug('unable to parse value to datetime')
        changed_timestamp = '1019-01-01T02:36:53.510Z'
    except TypeError:
        logging.debug('value has not been a string')
        changed_timestamp = '1019-01-01T02:36:53.510Z'
    return changed_timestamp


def change_value(dictionary, key_to_change, change_value_to):
    """
    :param dictionary: the event
    :param key_to_change: which key in the event should be changed
    :param change_value_to: can contain keywords or the value, which will replace the actual value
    :return:
    """
    logging.debug('change_value called with parameters: ' + key_to_change + ', ' + str(change_value_to))
    modified_dict = {}

    for key, value in dictionary.items():
        if key != key_to_change:
            if isinstance(value, MutableMapping):
                modified_dict[key] = change_value(value, key_to_change, change_value_to)
            else:
                modified_dict[key] = value
        else:
            if 'to_string' == change_value_to:
                modified_dict[key] = str(value)
            elif 'random_string' == change_value_to:
                modified_dict[key] = 'todo: generate random string'
            elif 'random_int' == change_value_to:
                modified_dict[key] = random.randint(-2, 100)
            elif 'random_timestamp' == change_value_to:
                modified_dict[key] = change_timestamp(value)
            elif 'delete_key' == change_value_to:
                pass
            else:
                modified_dict[key] = change_value_to

    return modified_dict


def process_event(event):
    logger.debug('processing event ')
    logger.debug(event)

    inject_fault = True if random.randint(0, 100) <= int(config.config['fault_injection_rate_in_percent']) else False

    if inject_fault:

        possible_fields_for_modification = utils.get_all_keys(event)
        logger.debug('possible keys for modification: ')
        logger.debug(possible_fields_for_modification)

        key_value_to_modify = random.choice(possible_fields_for_modification)
        possible_new_values = ['to_string', 'random_string', 'random_int', 'random_timestamp', 'delete_key']
        event = change_value(event, key_value_to_modify, random.choice(possible_new_values))

        logger.info('ran change_value_to on ' + key_value_to_modify)

    else:
        logger.info('did not modify event')

    logger.debug('remaining event:')
    logger.debug(event)

    return event
