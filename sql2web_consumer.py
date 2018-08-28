# -*- coding: utf-8 -*-
 
import sys
from kafka import KafkaConsumer,TopicPartition
import json
from serializer_contract import contract_deserializer
from kafka.structs import OffsetAndMetadata
__metaclass__ = type
 
 
class Consumer:
    def __init__(self, KafkaServer='127.0.0.1', KafkaPort='9092', GroupID='TestGroup', ClientId="wen", Topic='Test'):
        """
        用于设置消费者配置信息，这些配置项可以从源码中找到，下面为必要参数。
        :param KafkaServer: kafka服务器IP
        :param KafkaPort: kafka工作端口
        :param GroupID: 消费者组ID
        :param ClientId: 消费者名称
        :param Topic: 主题
        """
        self._bootstrap_server = '{host}:{port}'.format(host=KafkaServer, port=KafkaPort)
        self._groupId = GroupID
        self._topic = Topic
        self._clientId = ClientId
 
    def consumeMsg(self):
        try:
            """
            初始化一个消费者实例，消费者不是线程安全的，所以建议一个线程实现一个消费者，而不是一个消费者让多个线程共享
            下面这些是可选参数，可以在初始化KafkaConsumer实例的时候传递进去
            enable_auto_commit 是否自动提交，默认是true
            auto_commit_interval_ms 自动提交间隔毫秒数
            """
            consumer = KafkaConsumer(self._topic, bootstrap_servers=self._bootstrap_server,group_id=self._groupId, client_id=self._clientId, enable_auto_commit=False, value_deserializer=contract_deserializer())
 
            """
            这里不需要显示的调用订阅函数，在初始化KafkaConsumer对象的时候已经指定了主题，如果主题字段不为空则会自动调用订阅函数，至于
            这个线程消费哪个分区则是自动分配的。如果你希望手动指定分区则就需要使用 assign() 函数，并且在初始的时候不输入主题。
            """
            # consumer.subscribe(self._topicList)
 
            # 返回一个集合
            print("当前消费的分区为：", consumer.partitions_for_topic(self._topic))
            print("当前订阅的主题为：", consumer.subscription())
 
            items = consumer.poll(timeout_ms=10,max_records=5000)
            for i in items:
                for j in items[i]:
                    if j.value["id"]==-1:
                        tp = TopicPartition(j.topic,j.partition)
                        consumer.commit({
                            tp: OffsetAndMetadata(j.offset,None)
                        })
                        list_con=[]
                    else:
                        list_con.append(j.value)
            return list_con
                #consumer.commit_async()
                
        except Exception as err:
            print(err)
 
 
def sql2web_consume():
    try:
        c = Consumer(KafkaServer='192.168.23.179',GroupID="SW-group",Topic='sql2web')
        items = c.consumeMsg()
    except Exception as err:
        print(err.message)
    return items
 
 