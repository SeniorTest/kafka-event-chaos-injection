# internal modules
import traceback
import binascii
import random
import json
import os
import logging

# external modules
from kafka import KafkaConsumer

# own imports
import config
import utils
import modifier
import producer

logger = logging.getLogger(__name__)

def consume_events(bootstrap_server, source_topic, destination_topic, modify=False, stage='develop'):
    logger.info('starting consumer for topic ' + source_topic + ' and stage ' + stage)
    try:
        if stage == 'develop':
            with open(os.path.dirname(os.path.abspath(__file__)) + '/happy_path.json') as events_file:
                consumer = json.load(events_file)

        else:
            consumer = KafkaConsumer(source_topic,
                                     group_id='keci',
                                     bootstrap_servers=[bootstrap_server],
                                     value_deserializer=lambda v: binascii.unhexlify(v).decode('utf-8'))

        for msg in consumer:

            if modify:
                modified_event = process_event(msg)
            else:
                modified_event = msg

            producer.send_kafka_event(bootstrap_server, destination_topic, json.dumps(modified_event))

    except:
        logging.exception(traceback.print_exc())


def process_event(event):
    logger.debug('processing event ')
    logger.debug(event)
    inject_fault = True if random.randint(0, 100) <= int(config.config['fault_injection_rate_in_percent']) else False

    if inject_fault:
        possible_fields_for_modification = utils.get_all_keys(event)
        # select fault injection type
        # type: drop_key_value, change_value
        list_of_fault_injection_types = ['drop_key_value', 'change_value']
        select_injection_type = list_of_fault_injection_types[random.randint(0, len(list_of_fault_injection_types) - 1)]
        logger.debug('selected injection type: ' + select_injection_type)
        key_value_to_modify = possible_fields_for_modification[
            random.randint(0, len(possible_fields_for_modification) - 1)]

        if select_injection_type == 'drop_key_value':
            event = modifier.delete_keys_from_dict(event, [key_value_to_modify])

        elif select_injection_type == 'change_value':
            event = modifier.modify_value_in_dict(event, [key_value_to_modify])

        logger.info('run ' + select_injection_type + ' on ' + key_value_to_modify)

    else:
        logger.info('did not modify event')

    logger.debug('remaining event:')
    logger.debug(event)

    return event
