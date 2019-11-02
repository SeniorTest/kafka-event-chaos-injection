import traceback
import logging

# external modules
from kafka import KafkaProducer


def send_kafka_event(topic, raw_string):
    data = raw_string.encode('utf-8')

    try:
        logging.info('trying to send ' + raw_string + ' to topic ' + topic)
        producer = KafkaProducer(bootstrap_servers=['broker1:1234'])
        future = producer.send(topic, b'raw_bytes')
    except:
        print(traceback.print_exc())
