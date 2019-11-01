# internal modules
import traceback
import binascii
import random
import time
import json
import os

# external modules
from kafka import KafkaConsumer

# own imports
from source import utils
from source import modifier
from source import producer


def consume_events(source_topic, destination_topic, modify=False, stage='develop'):
    print('starting consumer for topic ' + source_topic + ' and stage ' + stage)
    try:
        if stage == 'develop':
            with open(os.path.dirname(os.path.abspath(__file__)) + './happy_path.json') as events_file:
                consumer = json.load(events_file)

        else:
            consumer = KafkaConsumer(source_topic,
                                     group_id='keci',
                                     bootstrap_servers=['localhost:9092'],
                                     value_deserializer=lambda v: binascii.unhexlify(v).decode('utf-8'))

        for msg in consumer:
            print(source_topic)
            print(time.sleep(5))
            if modify:
                modified_event = dispatch_event(msg)
            else:
                modified_event = msg

            producer.send_kafka_event(destination_topic, json.dumps(modified_event))

    except:
        print(traceback.print_exc())


def dispatch_event(event):
    print()
    possible_fields_for_modification = utils.get_all_keys(event)
    print(possible_fields_for_modification)
    # select fault injection type
    # type: drop_key_value, change_value
    list_of_fault_injection_types = ['drop_key_value', 'change_value']
    select_injection_type = list_of_fault_injection_types[random.randint(0, len(list_of_fault_injection_types) - 1)]
    print('selected injection type: ' + select_injection_type)
    key_value_to_modify = possible_fields_for_modification[random.randint(0, len(possible_fields_for_modification) - 1)]

    if select_injection_type == 'drop_key_value':
        event = modifier.delete_keys_from_dict(event, [key_value_to_modify])

    elif select_injection_type == 'change_value':
        event = modifier.modify_value_in_dict(event, [key_value_to_modify])

    print('run ' + select_injection_type + ' on ' + key_value_to_modify)
    print('remaining event:')
    print(event)

    return event
