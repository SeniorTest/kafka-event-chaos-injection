from source import producer


def test_send_data():
    # given
    data = 'bla'

    producer.send_kafka_event('test_topic',  data)