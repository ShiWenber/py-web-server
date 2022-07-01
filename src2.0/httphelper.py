import http
from importlib.resources import path
from os import pathsep
from sys import argv
from http.server import BaseHTTPRequestHandler, HTTPServer

import socketserver

import json

# import urlparse

import subprocess
from tracemalloc import start
from urllib.parse import urlparse
import os
import cgi


class Httptool(BaseHTTPRequestHandler):

    def _set_headers(self):

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self, INPUT_PATH):
        # self._set_headers()
        # parsed_path = urlparse.urlparse(self.path)
        # request_id = parsed_path.path
        # response = subprocess.check_output(["python", request_id])
        # self.wfile.write(json.dumps(response))
        paths = self.path
        print(paths)
        query = urllib.splitquery(paths)
        datas = query[1]
        models = datas
        path = str(query[0])
        enc = "UTF-8"
        if path[:13] == "/download/zip":  # 判断下载路径
            fn = os.path.join(INPUT_PATH, models+".zip")  # 下载文件地址
            try:
                resultf = open(fn, 'rb')  # 以读的形式打开下载文件
            except BaseException:
                self.send_response(200)  # 请求下载的文件不存在返回文件不存在报文
                self.send_header("Content-type", "text/html;charset=%s" % enc)
                self.end_headers()
                print("不存在")
                buf = "获取扫描数据失败，请重新获取数据"
            else:
                self.send_response(200)  # 文件存在返回状态码
                # 返回请求格式为"application/octet-stream"
                self.send_header("Content-type", "application/octet-stream")
                self.end_headers()
                buf = resultf.read()  # 读取文件发送给客户端
            self.wfile.write(buf)

    def do_Post(self, path):
        enc = "utf-8"  # 编码格式
        path = str(self.path)  # 获取请求路径
        print(path)
        length = int(self.headers['Content-Length'])  # 获取请求长度
        datas = urlparse.parse_qs(self.rfile.read(
            length).decode(enc), keep_blank_values=1)  # 获取请求数据
        if path == "/scandatas":
            models = datas['models'][0]  # 获取models参数数据
            # ---------
            pass
            # ---------

            # 返回报文
            self.send_response(200)  # 返回状态码
            self.send_header(
                'Content-type', f"text/html;charset={enc}")  # 返回报文头
            self.send_headers()  # 返回报文结束符
            buf = {
                "status": 0,
                "data": {
                    "filepath": "上传成功"
                }
            }
            self.wfile.write(json.dumps(buf).encode(enc))  # 返回报文体json格式
        if path == "/download":
            models = datas['models'][0]  # 获取models参数数据
            self.send_response(200)  # 返回状态码
            self.send_header(
                'Content-type', f"text/html;charset={enc}")  # 返回报文头
            self.end_headers
            buf = {
                "status": 0,
                "data": {
                    "filepath": "./download/zip/" + models + ".zip?" + models  # 返回文件下载路径
                }
            }
            self.wfile.write(json.dumps(buf).encode(enc))  # 返回报文体json格式

        if path == "/upload":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'post',
                         'CONTENT_TYPE': self.headers['Content-Type']
                         }
            )
            models = form['models'].value  # 获取models参数值
            datas = form['file'].value  # 获取上传文件内容
            fname = models+".zip"
            fn = os.path.join(INPUTF_PATH, fname)  # 生成文件存储路径
            outf = open(fn, 'wb')  # 写打开文件
            outf.write(datas)  # 将接收到的内容写入文件
            outf.close()  # 关闭文件
            self.send_response(200)
            self.send_header("Content-type", "text/html;charset=%s" % enc)
            self.send_header("test", "This is test!")
            self.end_headers()
            buf = {"status": 0,
                   "data": {
                       "msg": u"上传成功"}}
            self.wfile.write(json.dumps(buf))
        # if path == 

    def do_HEAD(self):
        self._set_headers()

    # def run(server_class=HTTPServer, handler_class=Httptool, port=8000):
    #     server_address = ('', port)

    #     httpd = server_class(server_address, handler_class)

    #     print('Starting httpd...')

    #     httpd.serve_forever()
def start_server(port):
    http_server = HTTPServer(('', port), Httptool)
    http_server.serve_forever()


if __name__ == "__main__":
    start_server(8000)

# if __name__ == "__main__":

#     if len(argv) == 2:

#         run(port=int(argv[1]))

#     else:

#         run()
