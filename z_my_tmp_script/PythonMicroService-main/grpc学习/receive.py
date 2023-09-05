# -*- coding: utf-8 -*-
import logging
import sys
sys.path.append(r'D:\HempHas\ProjectFile\PythonMicroService')
sys.path.append(r'D:\HempHas\ProjectFile\PythonMicroService\grpc学习\grpc_file')

import grpc
import time
import datetime
from concurrent import futures
import grpc_file
import jieba
import re
from google.protobuf.wrappers_pb2 import BoolValue
from grpc_file import ReceiveData_pb2_grpc

jieba.setLogLevel(log_level=0)
pattern = re.compile('(?:https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)


class ReceiveDataServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def match_url(self, text):
        """
            # 去除 URL
        :param text:
        :return:
        """
        clear = pattern.sub("", text)
        return clear

    def seg_sentence(self, data):
        """
            分词
        :param data:
        :return:
        """
        data = self.match_url(data)
        seg_text = jieba.cut(data.replace('\t', '').replace('\n', '').replace(" ", ''))
        context = "".join(seg_text)
        return context

    def receiveSample(self, request, context):
        """
            接收数据的 rpc 服务接口,
            该函数名 要和 ReceiveData.proto 文件中定义函数名一致
        :param request:
        :param context:
        :return:
        """
        request_list = request.reqList
        try:
            for item in request_list:
                text = item.text.replace('\n', '。').replace('\r', '。')
                text = self.seg_sentence(text)
                print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
                            '*** 添加标签：{}，添加文本：{}... ***'.format(item.labelValue, text[:10]))

            return BoolValue(value=True)
        except Exception as e:
            return BoolValue(value=False)


def server(host, port):
    # 1. 启动 rpc 服务
    server_rpc = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    ReceiveData_pb2_grpc.add_LabelServiceServicer_to_server(ReceiveDataServer(host, port), server_rpc)
    server_rpc.add_insecure_port("{}:{}".format(host, port))
    server_rpc.start()
    print('Grpc server connect successful!')

    try:
        while True:
            time.sleep(600)
            print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    except KeyboardInterrupt:
        print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
        server_rpc.stop(0)


if __name__ == '__main__':
    server(host='127.0.0.1', port=50001)
