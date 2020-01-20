# internal modules
import traceback
import json
import os
import logging
import hashlib

# external modules
from kafka import KafkaConsumer

# own imports
import modifier
import producer

logger = logging.getLogger(__name__)


def consume_events(bootstrap_server, source_topic, destination_topic, stage='develop'):
    logger.info('starting consumer for topic ' + source_topic + ' and stage ' + stage)
    logger.debug(bootstrap_server)

    list_of_self_send = list()

    try:
        if stage == 'develop':
            with open(os.path.dirname(os.path.abspath(__file__)) + '/happy_path.json') as events_file:
                consumer = json.load(events_file)

        else:
            topics = [source_topic, destination_topic]
            logger.debug(topics)
            consumer = KafkaConsumer(*topics,
                                     group_id='keci_' + destination_topic,
                                     bootstrap_servers=[bootstrap_server])

        for msg in consumer:
            logger.debug('')
            logger.info('--------------------------- receiving event ---------------------------')
            logger.info(
                'processing kafka event for topic ' + msg.topic + ' on partition ' + str(
                    msg.partition) + ' and key ' + str(msg.key))
            logger.debug(msg.value)
            hashed_messsage = hashlib.md5(msg.value).hexdigest()
            logger.debug(hashed_messsage)

            if hashed_messsage in list_of_self_send:
                logger.debug('ignoring message since its hash is in the self_send_list')
            else:
                logger.debug('message has not been send by myself')
                try:
                    msg_value = json.loads(msg.value)

                    if msg.topic == source_topic:
                        modified_event = modifier.process_event(msg_value)
                    else:
                        modified_event = msg_value

                    if msg.topic == source_topic:
                        send_to_topic = destination_topic
                    elif msg.topic == destination_topic:
                        send_to_topic = source_topic

                    producer.send_kafka_event(bootstrap_server, send_to_topic, json.dumps(modified_event))

                    hash_object = hashlib.md5(json.dumps(modified_event).encode())
                    logger.debug('---- adding message with ' + hash_object.hexdigest() + ' to list of send messages')
                    list_of_self_send.append(hash_object.hexdigest())
                    # reduce list size to 10
                    list_of_self_send = list_of_self_send[-10:]
                    logger.debug(list_of_self_send)

                except:
                    logger.exception('unable to load json from message')

        logging.info('finished consuming events')

    except:
        logging.exception(traceback.print_exc())
