from app_src import producer


def test_send_data():
    # given
    data = 'bla'

    producer.send_kafka_event('test_bootstrap_server', 'test_topic',  data)