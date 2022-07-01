from requests import head
import re
import socket


class request:
    request_message = b""
    req_mes_lines = b""
    request_line = b""
    head_lines = b""

    url = b""
    file_name = b""
    method = b""

    def __init__(self, client):
        self.request_message = client.recv(1024)
        self.req_mes_lines = self.request_message.splitlines()
        # GET /index.html HTTP/1.1 请求行
        self.request_line = self.req_mes_lines[0]
        self.header_lines = self.req_mes_lines[1:]  # 首部行

        # /index.html 获取相对url
        self.url = self.request_line.split()[1]
        # 提取用户请求的文件名
        self.file_name = re.match(r"\w+ +(/[^  ]*) ",
                                  self.request_line.decode("utf_8")).group(1)
        # 请求方法
        self.method = re.match(r"(\w+) +/[^ ]* ",
                               self.request_line.decode("utf-8")).group(1)

    def get_request_message(self):
        return self.request_message

    
    def get_url(self):
        return self.url

    def get_file_name(self):
        return self.file_name

    def get_method(self):
        return self.method
