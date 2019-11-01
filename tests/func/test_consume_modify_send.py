# internal imports
from multiprocessing import Process

from source import consumer


def test_app():
    t1 = Process(target=consumer.consume_events, args=('inbound_topic', 'outbound_topic', True, 'develop', ))
    t2 = Process(target=consumer.consume_events, args=('outbound_topic', 'inbound_topic', False, 'develop', ))
    t1.start()
    t2.start()
