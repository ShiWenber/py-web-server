# -*- coding:utf-8 -*-

# 导入模块
import multiprocessing
from pdb import post_mortem
import socket
import re
from sqlite3 import connect
from tkinter.tix import Tree  # 正则
import os

from request import Request


# 设置静态文件根目录
HTML_ROOT_DIR = "."


def process_connection(client):
    """总处理，连接所有功能模块

    处理客户端的连接：接受数据->解析命令->处理请求资源->（打包返回数据）

    Args:
        client (socket.socket): socket.socket对象
    """
    print("新连接：", client.getpeername())
    # 接受客户端发来的数据
    # client.settimeout(5) # 设置recv的超时时间
    # client.settimeout(None)

    req = Request(client)
    # 打印接受的数据
    print("接受的请求数据：", req.get_request_message)
    print("请求完整路径：", HTML_ROOT_DIR + req.get_file_name)

    if req.get_method == "GET":
        req.do_get()
    elif req.get_method == "POST":
        req.do_post()


def main():
    # 用于设置服务器绑定的地址
    WebServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP

    # 允许端口复用
    WebServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 将服务器绑定到指定的地址上
    WebServer.bind(('127.0.0.1', 8890))  # 0-65535:0-1024给操作系统使用

    print("服务器启动成功，等待客户端连接...")
    ip, port = WebServer.getsockname()
    print("服务器地址：", "http://"+str(ip)+":"+str(port))

    # windows下自动浏览器自动打开网页
    os.popen("start http://"+str(ip)+":"+str(port))

    # 服务端监听
    WebServer.listen(100)
    # 将套接字变为非堵塞
    WebServer.setblocking(False)
    client_socket_list = list()

    while True:  # 链接循环
        # 等待客户端请求连接
        try:
            client, addr = WebServer.accept()
            print("got connection from", addr)
            client.setblocking(False)
            client_socket_list.append(client)
        except Exception as ret:
            pass

        for client in client_socket_list:
            # 创建一个进程处理
            sub_p = multiprocessing.Process(
                target=process_connection, args=(client,))
            sub_p.start()
            # 关闭链接
            client.close()
            client_socket_list.remove(client)
    # 关闭这个链接
    client.close()


if __name__ == '__main__':
    main()
