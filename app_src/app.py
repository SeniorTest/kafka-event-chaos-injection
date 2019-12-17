# internal imports
from multiprocessing import Process
import traceback
import logging

# own imports
import config
import consumer



logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)


try:
    logger.info('trying to start consumer processes')
    logger.debug(config.config['bootstrap_server'])

    # create two consumers
    t1 = Process(target=consumer.consume_events, args=(config.config['bootstrap_server'], config.config['inbound_topic'], config.config['outbound_topic'], True, config.config['stage'], ))
    t2 = Process(target=consumer.consume_events, args=(config.config['bootstrap_server'], config.config['outbound_topic'], config.config['inbound_topic'], False, 'stage', ))
    t1.start()
    t2.start()
except:
    logger.exception('exception on starting consumer process')
    logger.exception(traceback.print_exc())