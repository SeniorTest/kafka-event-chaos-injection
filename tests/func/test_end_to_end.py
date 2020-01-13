import json
from datetime import datetime

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import pytest

# own imports
# renamed due to k8s config
import app_src.config as app_config


@pytest.fixture
def k8s_api():
    config.load_kube_config()
    c = Configuration()
    c.assert_hostname = False
    Configuration.set_default(c)
    core_v1 = core_v1_api.CoreV1Api()
    return core_v1


def exec_commands(api_instance, pod_name, commands):
    name = pod_name
    output = list()
    resp = None
    try:
        resp = api_instance.read_namespaced_pod(name=name,
                                                namespace='default')
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)

    # Calling exec interactively
    exec_command = ['/bin/bash']
    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  name,
                  'default',
                  command=exec_command,
                  stderr=True, stdin=True,
                  stdout=True, tty=False,
                  _preload_content=False)

    while resp.is_open():
        resp.update(timeout=1)
        if resp.peek_stdout():
            # last element removed since it is always empty
            output.extend(resp.read_stdout().split('\n')[:-1])
        if resp.peek_stderr():
            print("STDERR: %s" % resp.read_stderr())
        if commands:
            c = commands.pop(0)
            print("Running command... %s\n" % c)
            resp.write_stdin(c + "\n")
        else:
            print('no more commands to apply')
            break

    print('closing connection')
    resp.close()
    return output


def test_end_to_end(k8s_api):
    # todo: check for result not working, kafka-consumer does not return the latest event
    # to verify result, use kafka-console-consumer.sh on kafka pod manually
    # GIVEN
    kafka_pod = 'kafka-0'
    test_event = {"datetime": str(datetime.now()), "id": "070b6b16-626e-471f-8b5c-65173ff74a42", "name": "Order",
                  "source": "Broker", "timestamp": str(datetime.now())}
    formatted_test_event = json.dumps(test_event)

    commands_for_test_event_creation = [
        "kafka-console-producer.sh --broker-list " + app_config.config['bootstrap_server'] + " --topic " +
        app_config.config['topic_to_modify'],
        formatted_test_event
    ]

    commands_for_event_consumption = [
        "kafka-console-consumer.sh --bootstrap-server " + app_config.config['bootstrap_server'] + " --topic " +
        app_config.config['topic_to_not_touch'] + " --from-beginning" + " --group test_consumer_group"
    ]
    # WHEN
    exec_commands(k8s_api, kafka_pod, commands_for_test_event_creation)
    # THEN
    print(commands_for_event_consumption)
    result_list = exec_commands(k8s_api, kafka_pod, commands_for_event_consumption)
    print('received list of events')
    print(result_list)
    for result in result_list:
        print('-------------------')
        try:
            print(json.loads(result))
            received_event = json.loads(result)
            print(list(received_event.keys()))
            print(list(test_event.keys()))
            if len(list(received_event.keys())) == len(list(test_event.keys())):
                print('value must have been changed to bla')
                print(list(received_event.values()))
                assert 'bla' in list(received_event.values())
            else:
                print('key must have been dropped')
                print(list(set(list(received_event.keys())) - set(list(test_event.keys()))))
                assert len(list(received_event.keys())) < len(list(test_event.keys()))
        except json.decoder.JSONDecodeError:
            print('unable to decode as json')
            print(result)
