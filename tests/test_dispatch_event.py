# internal imports
import json
import os

# own imports
from source import consumer


def test_dispatch_event():
    # given
    event = {'id': '2550064a-a5da-4302-a391-13db3d60fc5e', 'name': 'TestEvent', 'source': 'TestSource',
             'timestamp': '2019-01-01T02:36:53.510Z',
             'nestedObject': {'nestedContent': '0000000c-0000-0000-0000-00000000000e'}
             }
    # when
    modified_event = consumer.dispatch_event(event)
    # then
    assert modified_event is not None
    assert modified_event is not event


def test_dispatch_events():
    # given
    with open(os.path.dirname(os.path.abspath(__file__)) + './happy_path.json') as events_file:
        event_list = json.load(events_file)

    for event in event_list:
        # when
        received_event = consumer.dispatch_event(event)
        # then
        assert received_event is not None
