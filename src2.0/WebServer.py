# -*- coding:utf-8 -*-

# 导入模块
import multiprocessing
import socket
import re
from sqlite3 import connect
from tkinter.tix import Tree  # 正则
import os


# 设置静态文件根目录
HTML_ROOT_DIR = "."

def do_post(client, request_message):
    print()
    try:
        # req_datas = 
        print("post接受的请求数据：\n", request_message)
    except Exception as e:
        return 
    else:
        response_start_line = bytes("HTTP/1.1 404 Not Found\r\n", "utf-8")
        response_header = bytes("Server:My server\r\n", "utf-8")
        response_body = bytes(" 测试 这是post响应的请求!", "utf-8")
    
        # 构造响应数据
    response_data = response_start_line + response_header + bytes("\r\n", "utf_8") + response_body
    # print("返回数据：", response_data)  # 打印一下返回数据

    # 向客户端返回响应数据
    client.send(response_data)

    # 关闭客户端连接
    # client.close()
        
    
def process_connection(client):
    """处理客户端的连接：接受数据->解析命令->处理请求资源->（打包返回数据）"""
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
    header_lines = req_mes_lines[1:]  # 首部行
    
    print(req_mes_lines[0])
    print(req_mes_lines[3])
    length = req_mes_lines[3].decode("utf-8").split(":")
    print(length[1])

    # 提取用户请求的文件名
    file_name = re.match(r"\w+ +(/[^  ]*) ", request_line.decode("utf_8")).group(1)
    # 请求方法
    method = re.match(r"(\w+) +/[^ ]* ", request_line.decode("utf-8")).group(1)

    print("请求完整路径：", HTML_ROOT_DIR + file_name)

    if method == "GET":

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
            response_header += bytes("Content-Length:%d\r\n" % len(response_body), "utf-8")

        # 构造响应数据
        response_data = response_start_line + response_header + bytes("\r\n", "utf_8") + response_body
        # print("返回数据：", response_data)  # 打印一下返回数据

        # 向客户端返回响应数据
        client.send(response_data)

        # 关闭客户端连接
        # client.close()

    elif method == "POST":
        do_post(client, request_message)



def main():
    # 用于设置服务器绑定的地址
    WebServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP

    # 允许端口复用
    WebServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 将服务器绑定到指定的地址上
    WebServer.bind(('127.0.0.1', 8889))  # 0-65535:0-1024给操作系统使用
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
            sub_p = multiprocessing.Process(target=process_connection, args=(client,))
            sub_p.start()
            # 关闭链接
            client.close()
            client_socket_list.remove(client)
    # 关闭这个链接
    client.close()


if __name__ == '__main__':
    main()
