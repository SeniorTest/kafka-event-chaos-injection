import pytest

# own imports
import app_src.utils
import app_src.modifier


@pytest.mark.parametrize('key_to_alter, change_value_to', [('id', 'bla'), ('nestedContent', 'nestedBla')])
def test_alter_value(key_to_alter, change_value_to):
    # given
    event = {'id': '2550064a-a5da-4302-a391-13db3d60fc5e', 'name': 'TestEvent', 'source': 'TestSource',
             'timestamp': '2019-01-01T02:36:53.510Z',
             'nestedObject': {'nestedContent': '0000000c-0000-0000-0000-00000000000e'}
             }
    given_value = app_src.utils.get_first_value_for(key_to_alter, event)
    # when
    received_event = app_src.modifier.change_value(event, key_to_alter, change_value_to)
    print(received_event)
    altered_value = app_src.utils.get_first_value_for(key_to_alter, received_event)
    # then
    assert given_value != altered_value


@pytest.mark.parametrize('key_to_alter, change_key_to', [('timestamp', 'random_timestamp'), ('timestamp', '3019-01-01T02:36:56.510Z')])
def test_alter_timestamp(key_to_alter, change_key_to):
    # given
    event = {'id': '2550064a-a5da-4302-a391-13db3d60fc5e', 'name': 'TestEvent', 'source': 'TestSource',
             'timestamp': '2019-01-01T02:36:53.510Z',
             'nestedObject': {'nestedContent': '0000000c-0000-0000-0000-00000000000e'}
             }

    given_value = app_src.utils.get_first_value_for(key_to_alter, event)
    # when
    received_event = app_src.modifier.change_value(event, key_to_alter, change_key_to)
    altered_value = app_src.utils.get_first_value_for(key_to_alter, received_event)
    print(altered_value)
    # then
    assert given_value != altered_value

    if change_key_to != 'random_timestamp':
        assert change_key_to == altered_value


def test_change_value_to_specific_value():
    # given
    event = {'id': '2550064a-a5da-4302-a391-13db3d60fc5e', 'name': 'TestEvent', 'source': 'TestSource',
             'timestamp': '2019-01-01T02:36:53.510Z',
             'nestedObject': {'nestedContent': '0000000c-0000-0000-0000-00000000000e'}
             }
    # when
    received_event = app_src.modifier.change_value(event, 'timestamp', change_value_to=123)
    # then
    print(received_event)
    assert received_event['timestamp'] == 123


def test_change_value_to_string():
    # given
    event = {'id': '2550064a-a5da-4302-a391-13db3d60fc5e', 'name': 'TestEvent', 'source': 'TestSource',
             'timestamp': '2019-01-01T02:36:53.510Z',
             'nestedObject': {'nestedContent': '0000000c-0000-0000-0000-00000000000e',
                              'quantity': 200}
             }
    # when
    received_event = app_src.modifier.change_value(event, 'quantity', change_value_to='to_string')
    # then
    assert isinstance(received_event['nestedObject']['quantity'], str)