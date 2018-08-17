import sys
import time
import json

from kafka import KafkaConsumer

KAFAKA_HOST = '127.0.0.1'
KAFAKA_PORT = 9092
KAFAKA_TOPIC = 'chuangF_U'
file_name = '.\json\chuang_f_u.json'
groupID = 'getall'

class Kafka_consumer():
    '''''
    消费模块: 通过不同groupid消费topic里面的消息
    '''

    def __init__(self, kafkahost, kafkaport, kafkatopic, filename,key='test1'):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.groupID = None
        self.consumer = KafkaConsumer(self.kafkatopic,  bootstrap_servers='{kafka_host}:{kafka_port}'.format(
                                          kafka_host=self.kafkaHost,
                                          kafka_port=self.kafkaPort),
                                        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                      auto_offset_reset='earliest',
                                      enable_auto_commit=False,
                                      )
        self.filename = filename

    def consume_data(self):
        try:
            for message in self.consumer:
                yield message

        except KeyboardInterrupt as e:
            print(e)

if __name__ == '__main__':
    my_consumer=KafkaConsumer(KAFAKA_TOPIC,  bootstrap_servers='{kafka_host}:{kafka_port}'.format(
                                          kafka_host=KAFAKA_HOST,
                                          kafka_port=KAFAKA_PORT),
                                        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                      auto_offset_reset='earliest',
                                      enable_auto_commit=False,
                                      )
    i = 0
    data={}
    data['data_number'] = 0
    json.dump(data, open(file_name, 'w'))
    for msg in my_consumer:
        data = json.load(open(file_name))
        data['data_number'] += 1
        data_str = 'data_%d' % (data['data_number'])
        data[data_str] = msg
        json.dump(data, open(file_name, 'w'))
        print(data['data_number'])