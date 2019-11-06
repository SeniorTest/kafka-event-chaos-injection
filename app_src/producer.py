import logging

# external modules
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

logger = logging.getLogger(__name__)

kafka_logger = logging.getLogger('kafka')
kafka_logger.setLevel(logging.WARNING)

def send_kafka_event(bootstrap_server, topic, raw_string):
    data = raw_string.encode('utf-8')

    try:
        logger.info('trying to send ' + raw_string + ' to topic ' + topic)
        producer = KafkaProducer(bootstrap_servers=[bootstrap_server])
        future = producer.send(topic, data)
    except NoBrokersAvailable:
        logger.exception('No brokers available')
