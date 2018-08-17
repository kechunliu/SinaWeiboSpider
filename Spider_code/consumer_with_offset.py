import sys
import time
import json
import os

from kafka import KafkaConsumer

KAFAKA_HOST = '127.0.0.1'
KAFAKA_PORT = 9092
KAFAKA_TOPIC = 'sinaweibo'
file_name = '.\json\data_offset.json'
offset_file_name = '.\json\offset.json'
groupID = 'get_all'


if __name__ == '__main__':
    if os.path.exists(offset_file_name):
        offset = json.load(open(offset_file_name))
        offset = offset['offset']
    else :
        offset = 0
        offset_json = {}
        offset_json['offset'] = 0
        json.dump(offset_json, open(offset_file_name, 'w'))
    my_consumer = KafkaConsumer(KAFAKA_TOPIC, bootstrap_servers='{kafka_host}:{kafka_port}'.format(
        kafka_host=KAFAKA_HOST,
        kafka_port=KAFAKA_PORT),
                                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                auto_offset_reset='earliest',
                                group_id = 'aaaa',
                                enable_auto_commit = False
                                )
    if os.path.exists(file_name):
        pass
    else :
        data = {}
        data['data_number'] = 0
        json.dump(data, open(file_name, 'w'))
    for msg in my_consumer:
        data = json.load(open(file_name))
        data['data_number'] += 1
        data_str = 'data_%d' % (data['data_number'])
        data[data_str] = msg
        json.dump(data, open(file_name, 'w'))
        print(data['data_number'])
