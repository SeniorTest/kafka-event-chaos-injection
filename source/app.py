# internal imports
from multiprocessing import Process
import traceback

# own imports
import consumer


try:
    # create two consumers
    t1 = Process(target=consumer.consume_events, args=('Credit_transac',))
    t2 = Process(target=consumer.consume_events, args=('Debit_transac',))
    t1.start()
    t2.start()
except:
    print(traceback.print_exc())
    print("Error: unable")