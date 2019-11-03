# internal imports
from collections.abc import MutableMapping


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
