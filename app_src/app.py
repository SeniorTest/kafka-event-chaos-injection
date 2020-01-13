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
    logger.info('trying to start consumer process')
    logger.debug(config.config['bootstrap_server'])

    t1 = Process(target=consumer.consume_events, args=(
        config.config['bootstrap_server'], config.config['topic_to_modify'], config.config['topic_to_not_touch'],
        config.config['stage'],))
    t1.start()
except:
    logger.exception('exception on starting consumer process')
    logger.exception(traceback.print_exc())
