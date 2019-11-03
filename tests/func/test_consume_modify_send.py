# internal imports
from multiprocessing import Process

import app_src.consumer


def test_app():
    t1 = Process(target=app_src.consumer.consume_events, args=('test_bootstrap_server', 'inbound_topic', 'outbound_topic', True, 'develop', ))
    t2 = Process(target=app_src.consumer.consume_events, args=('test_bootstrap_server', 'outbound_topic', 'inbound_topic', False, 'develop', ))
    t1.start()
    t2.start()
