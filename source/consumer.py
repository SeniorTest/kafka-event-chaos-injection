# internal modules
import traceback
import binascii
import random
import time


# external modules
from kafka import KafkaConsumer

# own imports
from source import utils
from source import modifier


def consume_events(topic):
    print('starting consumer for topic: ' + topic)
    try:
        consumer = KafkaConsumer(topic,
                                     group_id='keci',
                                     bootstrap_servers=['localhost:9092'],
                                     value_deserializer=lambda v: binascii.unhexlify(v).decode('utf-8'))

        for msg in consumer:
            print(topic)
            print(time.sleep(5))
            dispatch_event(msg)

            # msg=ast.literal_eval(msg.value)
            # if(msg[2] == 'C'):
            #     performCreditOperation(msg)
            # elif (msg[2] == 'D'):
            #     performDebitOperation(msg)
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
