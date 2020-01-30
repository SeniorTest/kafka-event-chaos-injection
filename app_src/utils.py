def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield (key, value)


def get_all_keys(dictionary):
    return [item[0] for item in list(recursive_items(dictionary))]


def get_first_value_for(key, dictionary):
    return [item[1] for item in list(recursive_items(dictionary)) if item[0] == key][0]
