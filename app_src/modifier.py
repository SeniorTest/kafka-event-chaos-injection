# internal imports
import logging
import random
from collections.abc import MutableMapping

# own imports
import config
import utils


logger = logging.getLogger(__name__)


def delete_keys_from_dict(dictionary, keys):
    keys_set = set(keys)

    modified_dict = {}
    for key, value in dictionary.items():
        if key not in keys_set:
            if isinstance(value, MutableMapping):
                modified_dict[key] = delete_keys_from_dict(value, keys_set)
            else:
                modified_dict[key] = value
    return modified_dict


def modify_value_in_dict(dictionary, keys):
    keys_set = set(keys)

    modified_dict = {}
    for key, value in dictionary.items():
        if key not in keys_set:
            if isinstance(value, MutableMapping):
                modified_dict[key] = modify_value_in_dict(value, keys_set)
            else:
                modified_dict[key] = value
        else:
            modified_dict[key] = 'bla'
    return modified_dict


def process_event(event):
    logger.debug('processing event ')
    logger.debug(event)
    inject_fault = True if random.randint(0, 100) <= int(config.config['fault_injection_rate_in_percent']) else False

    if inject_fault:
        possible_fields_for_modification = utils.get_all_keys(event)
        # select fault injection type
        # type: drop_key_value, change_value
        list_of_fault_injection_types = ['drop_key_value', 'change_value']
        selected_injection_type = list_of_fault_injection_types[random.randint(0, len(list_of_fault_injection_types) - 1)]
        logger.debug('selected injection type: ' + selected_injection_type)
        logger.debug('possible keys for modification: ')
        logger.debug(possible_fields_for_modification)
        key_value_to_modify = possible_fields_for_modification[
            random.randint(0, len(possible_fields_for_modification) - 1)]

        if selected_injection_type == 'drop_key_value':
            event = delete_keys_from_dict(event, [key_value_to_modify])

        elif selected_injection_type == 'change_value':
            event = modify_value_in_dict(event, [key_value_to_modify])

        logger.info('run ' + selected_injection_type + ' on ' + key_value_to_modify)

    else:
        logger.info('did not modify event')

    logger.debug('remaining event:')
    logger.debug(event)

    return event