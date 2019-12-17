import logging
import json

# external modules
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

logger = logging.getLogger(__name__)

kafka_logger = logging.getLogger('kafka')
kafka_logger.setLevel(logging.WARNING)


def send_kafka_event(bootstrap_server, topic, raw_string):

    try:
        logger.info('trying to send ' + raw_string + ' to topic ' + topic)
        producer = KafkaProducer(bootstrap_servers=[bootstrap_server]
                                 # value_serializer=lambda x: json.dumps(x).encode('utf-8')
                                 )
        future = producer.send(topic, value=bytes(raw_string, 'utf-8')).add_callback(on_kafka_send_success).add_errback(on_kafka_send_error)
        logger.debug(future)
        producer.flush()
    except NoBrokersAvailable:
        logger.exception('No brokers available')
    except:
        logger.exception('some other exception')


def on_kafka_send_success(record_metadata):
    logger.debug(record_metadata.topic)


def on_kafka_send_error(excp):
    kafka_error_message = "Error while sending kafka message :" + str(excp)
    raise Exception(excp)
