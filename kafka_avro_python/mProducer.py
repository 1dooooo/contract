# -*- coding: utf-8 -*-
from serializer_contract import contract_serializer,contract_deserializer
import random
import sys
from kafka import KafkaProducer
from kafka.client import log
import time
import json

from FutureContract import FutureContract
from db_about import DBSession

__metaclass__ = type
 
 
class Producer:
    def __init__(self, KafkaServer='127.0.0.1', KafkaPort='9092', ClientId="Procucer01", Topic=None):
        """
        用于设置生产者配置信息，这些配置项可以从源码中找到，下面为必要参数。
        :param KafkaServer: kafka服务器IP
        :param KafkaPort: kafka工作端口
        :param ClientId: 生产者名称
        :param Topic: 主题
        """
        self._bootstrap_server = '{host}:{port}'.format(host=KafkaServer, port=KafkaPort)
        self._topic = Topic
        self._clientId = ClientId
 
        """
        初始化一个生产者实例，生产者是线程安全的，多个线程共享一个生产者实例效率比每个线程都使用一个生产者实例要高
        acks: 消费者只能消费被提交的，而只有消息在所有副本中都有了才算提交，生产者发送了消息是否要等待所有副本都同步了该消息呢？这个值就是控制这个的。默认是1，表示只要该分区的Leader副本成功写入日志就返回。0表示生产者无需等待，发送完就返回；all是所有副本都写入该消息才返回。 all可靠性最高但是效率最低，0效率最高但是可靠性最低，所以一般用1。
        retries: 表示请求重试次数，默认是0，上面的acks配置请求完成的标准，如果请求失败，生产者将会自动重试，如果配置为0则不重试。但是如果重试则有可能发生重复发送消息。
        key_serializer: 键的序列化器，默认不设置，采用字节码
        value_serializer: 值得序列化器，默认不设置，采用字节码，因为可以发送单一字符，也可以发送键值型消息
        """
        try:
            
            self._producer = KafkaProducer(bootstrap_servers=self._bootstrap_server, client_id=self._clientId, acks=1,value_serializer=contract_serializer())
        except Exception as err:
            print(err.message)
    

    def _TIMESTAMP(self):
        t = time.time()
        return int((round(t * 1000)))
 
    # 时间戳转换为普通时间
    def getNormalTime(self, temp_timeStamp, timeSize=10):
        timeStamp = temp_timeStamp
        if timeSize == 13:
            timeStamp = int(temp_timeStamp / 1000)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime
 
    # 发送成功的回调函数
    def _on_send_success(self, record_metadata):
        print("Topic: %s Partition: %d Offset: %s" % (record_metadata.topic, record_metadata.partition, record_metadata.offset))
 
    # 发送失败的回调函数
    def _on_send_error(self, excp):
        log.error('I am an errback', exc_info=excp)
 
    def sendMsg(self, msg, partition=None):
        """
        发送消息
        :param msg: 消息
        :param partition: 分区也可以不指定
        :return:
        """
        if not msg:
            print("消息不能为空。")
            return None
 
        # 发送的消息必须是序列化后的，或者是字节

        message =msg
        try:
            TIMESTAMP = self._TIMESTAMP()
            # 发送数据，异步方式，调用之后立即返回，因为这里其实是发送到缓冲区，所以你可以多次调用，然后一起flush出去。
            self._producer.send(self._topic, partition=partition,value=message, timestamp_ms=TIMESTAMP).add_callback(self._on_send_success).add_errback(self._on_send_error)
            # 下面的 flush是阻塞的，只有flush才会真正通过网络把缓冲区的数据发送到对端，如果不调用flush，则等到时间或者缓冲区满了就会发送。
            self._producer.flush()
            #print(self.getNormalTime(TIMESTAMP, timeSize=13) + " send msg: " + str(message))
        except Exception as err:
            print(err)
 
 
def main():
    p = Producer(KafkaServer="192.168.23.179", KafkaPort="9092", Topic='one')
    #time.sleep(1)
    result = DBSession().query(FutureContract).all()
    s=DBSession().query(FutureContract.id, FutureContract.exchange, FutureContract.product).all()
    for item in result:
        p.sendMsg(item.to_raw_dict())
    writer.close()
    
        
 
 
if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit()