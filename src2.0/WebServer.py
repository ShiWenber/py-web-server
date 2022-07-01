# -*- coding:utf-8 -*-

# 导入模块
import multiprocessing
from pdb import post_mortem
import socket
import re
from sqlite3 import connect
from tkinter.tix import Tree  # 正则
import os


# 设置静态文件根目录
HTML_ROOT_DIR = "."


def entity_body(request_message):
    """提取实体主体

    Args:
        request_message (bytes): 请求报文

    Returns:
        bytes: 实体主题
    """
    # 提取实体主体
    entity_body = request_message.split(b"\r\n\r\n")[1]  # 切割出实体主体
    return entity_body

# 将username=shi&password=sjdif&sex=male字符串转化为字典


def to_postdict(entity_body):
    """将entity_body字符串转化为字典类型

    Args:
        entity_body (bytes str):实体主体

    Returns:
        dict:实体主体键值对
    """
    # 如果只有一个&，那么就判断为单键值对
    res = {}
    if entity_body.find(b"&") == -1 and entity_body.find(b"=") == -1:
        print("entity_body 非键值对形式")
        raise Exception("entity_body 非键值对形式")
    if entity_body.find(b"&") == -1:
        # 单键值对
        key = entity_body.split(b"=")[0]
        value = entity_body.split(b"=")[1]
        res[key] = value
        return res
    else:
        # 多键值对
        key_values = entity_body.split(b'&')
        for key_value in key_values:
            key, value = key_value.split(b'=')
            res[key] = value
        return res


def do_post(client, request_message, url):
    """post报文处理

    Args:
        client (socket.socket): socket.socket对象
        request_message (bytes): 请求报文
        url (bytes): 请求url
    """
    print(url)
    response_start_line = bytes("", "utf-8")
    response_header = bytes("", "utf-8")
    response_body = bytes("", "utf-8")
    try:
        # req_datas =
        print("post接受的请求数据：\n", request_message)
        # 用正则表达式提取request_message报文中的实体主体

        if url == b"/test":
            print("test")
            response_start_line = bytes("HTTP/1.1 404 Not Found\r\n", "utf-8")
            response_header = bytes("Server:My server\r\n", "utf-8")
            response_body = bytes("test", "utf-8")
        elif url == b"/print":
            response_start_line = bytes("HTTP/1.1 200 OK\r\n", "utf-8")
            response_header = bytes("Server:My server\r\n", "utf—8")
            postdict = to_postdict(entity_body(request_message))
            response_body = bytes(str(postdict), "utf-8")
        if url == b"/download":
            print("download")
            response_start_line = bytes("HTTP/1.1 200 OK\r\n", "utf-8")
            response_header = bytes("Server:My server\r\n", "utf—8")
            response_body = bytes("download", "utf-8")
    except Exception as e:
        print(e)
        response_start_line = bytes("HTTP/1.1 404 Not Found\r\n", "utf-8")
        response_header = bytes("Server:My server\r\n", "utf-8")
        response_body = bytes("there is something error!", "utf-8")

        # 构造响应数据
    response_data = response_start_line + response_header + \
        bytes("\r\n", "utf_8") + response_body
    # print("返回数据：", response_data)  # 打印一下返回数据

    # 向客户端返回响应数据
    client.send(response_data)

    # 关闭客户端连接
    # client.close()


def do_get(client, request_message, url, file_name):
    """get报文处理

    Args:
        client (socket.socket): socket.socket对象
        request_message (bytes): 请求报文
        url (bytes): 请求url
    """
    print(url)
    response_start_line = bytes("", "utf-8")
    response_header = bytes("", "utf-8")
    response_body = bytes("", "utf-8")
    if "/" == file_name:
        file_name = "/index.html"

        # 打开文件，读取内容
    try:
        file = open(HTML_ROOT_DIR + file_name, "rb")
    except IOError:
        response_start_line = bytes("HTTP/1.1 404 Not Found\r\n", "utf-8")
        response_header = bytes("Server:My server\r\n", "utf-8")
        response_body = bytes("The file is not found!", "utf-8")
    else:
        file_data = file.read()
        file.close()
        response_body = file_data
        response_start_line = bytes("HTTP/1.1 200 OK\r\n", "utf_8")
        response_header = bytes("Server:My server\r\n", "utf—8")
        response_header += bytes("Content-Length:%d\r\n" %
                                 len(response_body), "utf-8")
    # 构造响应数据
    response_data = response_start_line + response_header + \
        bytes("\r\n", "utf_8") + response_body
    # print("返回数据：", response_data)  # 打印一下返回数据
    # 向客户端返回响应数据
    print("响应报文：", response_data)
    client.send(response_data)
    # 关闭客户端连接
    # client.close()


def process_connection(client):
    """总处理，连接所有功能模块

    处理客户端的连接：接受数据->解析命令->处理请求资源->（打包返回数据）

    Args:
        client (socket.socket): socket.socket对象
    """
    print("新连接：", client.getpeername())
    # 接受客户端发来的数据
    # client.settimeout(5) # 设置recv的超时时间
    request_message = client.recv(1024)
    # client.settimeout(None)
    # 打印接受的数据
    print("接受的请求数据：", request_message)

    # # -------------

    # 请求 message(报文)

    # - request line(请求行): method(GET POST HEAD PUT DELETE), URL, protocol
    # - header line(首部行):
    # - entity body:
    # # -------------

    # 处理请求
    req_mes_lines = request_message.splitlines()

    request_line = req_mes_lines[0]  # GET /index.html HTTP/1.1 请求行
    url = request_line.split()[1]  # /index.html 获取相对url
    header_lines = req_mes_lines[1:]  # 首部行

    print(req_mes_lines[0])
    print(req_mes_lines[3])
    length = req_mes_lines[3].decode("utf-8").split(":")
    print(length[1])

    # 提取用户请求的文件名
    file_name = re.match(r"\w+ +(/[^  ]*) ",
                         request_line.decode("utf_8")).group(1)
    # 请求方法
    method = re.match(r"(\w+) +/[^ ]* ", request_line.decode("utf-8")).group(1)

    print("请求完整路径：", HTML_ROOT_DIR + file_name)

    if method == "GET":
        do_get(client, request_message, url, file_name)
    elif method == "POST":
        do_post(client, request_message, url)


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
