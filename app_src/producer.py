import traceback
import logging

# external modules
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


def send_kafka_event(bootstrap_server, topic, raw_string):
    data = raw_string.encode('utf-8')

    try:
        logging.info('trying to send ' + raw_string + ' to topic ' + topic)
        producer = KafkaProducer(bootstrap_servers=[bootstrap_server])
        future = producer.send(topic, b'raw_bytes')
    except NoBrokersAvailable:
        logging.exception('No brokers available')
