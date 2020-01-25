import pytest

# own imports
import app_src.utils
import app_src.modifier


@pytest.mark.parametrize('key_to_delete', ['id', 'nestedContent'])
def test_drop_key_value(key_to_delete):
    # given
    event = {'id': '2550064a-a5da-4302-a391-13db3d60fc5e', 'name': 'TestEvent', 'source': 'TestSource',
             'timestamp': '2019-01-01T02:36:53.510Z',
             'nestedObject': {'nestedContent': '0000000c-0000-0000-0000-00000000000e'}
             }
    # when
    received_event = app_src.modifier.__delete_keys_from_dict(event, [key_to_delete])
    # then
    assert key_to_delete not in app_src.utils.get_all_keys(received_event)


@pytest.mark.parametrize('key_to_alter', ['id', 'nestedContent'])
def test_alter_value(key_to_alter):
    # given
    event = {'id': '2550064a-a5da-4302-a391-13db3d60fc5e', 'name': 'TestEvent', 'source': 'TestSource',
             'timestamp': '2019-01-01T02:36:53.510Z',
             'nestedObject': {'nestedContent': '0000000c-0000-0000-0000-00000000000e'}
             }
    given_value = [item[1] for item in list(app_src.utils.recursive_items(event)) if item[0] == key_to_alter]
    # when
    received_event = app_src.modifier.__modify_value_in_dict(event, [key_to_alter])
    altered_value = [item[1] for item in list(app_src.utils.recursive_items(received_event)) if item[0] == key_to_alter]
    # then
    assert given_value != altered_value


@pytest.mark.parametrize('key_to_alter', ['timestamp'])
def test_alter_timestamp(key_to_alter):
    # given
    event = {'id': '2550064a-a5da-4302-a391-13db3d60fc5e', 'name': 'TestEvent', 'source': 'TestSource',
             'timestamp': '2019-01-01T02:36:53.510Z',
             'nestedObject': {'nestedContent': '0000000c-0000-0000-0000-00000000000e'}
             }

    given_value = [item[1] for item in list(app_src.utils.recursive_items(event)) if item[0] == key_to_alter]
    # when
    received_event = app_src.modifier.__modify_timestamp(event, [key_to_alter])
    altered_value = [item[1] for item in list(app_src.utils.recursive_items(received_event)) if item[0] == key_to_alter]
    # then
    assert given_value != altered_value