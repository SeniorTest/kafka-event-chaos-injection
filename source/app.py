# internal imports
from multiprocessing import Process
import traceback
import logging

# own imports
import consumer


logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)

try:
    logger.info('trying to start consumer processes')
    # create two consumers
    t1 = Process(target=consumer.consume_events, args=('inbound_topic', 'outbound_topic', True, 'develop', ))
    t2 = Process(target=consumer.consume_events, args=('outbound_topic', 'inbound_topic', False, 'develop', ))
    t1.start()
    t2.start()
except:
    logger.exception('exception on starting consumer process')
    logger.exception(traceback.print_exc())
