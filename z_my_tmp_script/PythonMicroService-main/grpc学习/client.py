# -*- coding: utf-8 -*-
import sys
sys.path.append('D:\HempHas\ProjectFile\PythonMicroService\grpc学习\grpc_file')
import grpc
from grpc_file import ReceiveData_pb2, ReceiveData_pb2_grpc


def run():
    # 1. 连接 rpc 服务 , ip和端口号 要一致

    channel = grpc.insecure_channel('127.0.0.1:50001')

    # 2. 调用 rpc
    stub = ReceiveData_pb2_grpc.LabelServiceStub(channel)
    request_list = ReceiveData_pb2.SampleRequestList()
    for data in range(1022):
        label = str(data)
        text = '第{}个标签数据'.format(label)
        # 由于我们在proto文件中定义的接收数据格式为List，所以这里我们需要先定义一个向List中添加数据的对象
        request = request_list.reqList.add()
        request.labelValue = label
        request.text = text
    response = stub.receiveSample(request_list)
    print(response)


if __name__ == '__main__':
    run()
