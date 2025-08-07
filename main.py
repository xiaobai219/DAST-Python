#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import asyncio
import threading

from mitmproxy.http import HTTPFlow
from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster
from multiprocessing import Process

import util.log
from app import create_app
from app.source import commontParams
from scanner.api_scanner import api_collection
from scanner.dast_scanner import dast_scan

logger = util.log.get_logger()
app = create_app()

black_path = [
            ".html",
            # 样式文件
            ".css", ".less", ".scss",
            # 脚本文件
            ".js", ".mjs",
            # 图片文件
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico",
            # 字体文件
            ".woff", ".woff2", ".ttf", ".eot",
            # 其他静态资源
            ".map", ".json", ".txt", ".xml", ".pdf", ".mp3", ".mp4", ".webm", ".ogg"
        ]
black_type = [
            "text/css",
            "application/javascript",
            "application/x-javascript",
            "image/png",
            "image/jpeg",
            "image/gif",
            "image/svg+xml",
            "image/webp",
            "font/woff",
            "font/woff2",
            "font/ttf",
            "application/font-woff",
            "text/plain",
            "text/html",
            "application/xhtml+xml"
]

black_methods = [
    "HEAD",
    "OPTIONS"
]

dast_req_id = {}
api_req_id = {}


class Counter:
    def request(self, flow: HTTPFlow):
        host = flow.request.host + ":" + str(flow.request.port)
        path = flow.request.path
        lower_path = path.lower()
        url = flow.request.url
        for ext in black_path:
            if lower_path.endswith(ext):
                return
        print(commontParams.rules)
        for rule in commontParams.rules:
            if host in rule:
                dast_req_id[flow.id] = {"request": flow.request, 'rules': rule[host], "department": rule["department"], "businessline": rule["businessline"]}

        print(commontParams.api_collection_rules)
        for rule in commontParams.api_collection_rules:
            if url.startswith(rule["url"]):
                api_req_id[flow.id] = {"request": flow.request, "department": rule["department"], "businessline": rule["businessline"]}

    def response(self, flow: HTTPFlow):
        if flow.id in dast_req_id:
            request = dast_req_id[flow.id]["request"]
            rules = dast_req_id[flow.id]["rules"]
            department = dast_req_id[flow.id]["department"]
            businessline = dast_req_id[flow.id]["businessline"]
            del dast_req_id[flow.id]
            content_type = flow.response.headers.get("Content-Type", "").lower()
            # 提取主类型和子类型（例如：text/html; charset=utf-8 → text/html）
            if ";" in content_type:
                content_type = content_type.split(";")[0].strip()
            # 判断是否为静态文件
            if content_type in black_type:
                return
            if flow.response.status_code == 200:
                # 创建一个新线程来执行修改后的请求
                for r in rules:
                    if r["ruleMethod"] == "*":
                        threading.Thread(target=dast_scan, args=(request, flow.response, r, department, businessline)).start()
                    elif r["ruleMethod"] == request.method:
                        threading.Thread(target=dast_scan, args=(request, flow.response, r, department, businessline)).start()

        if flow.id in api_req_id:
            request = api_req_id[flow.id]["request"]
            department = api_req_id[flow.id]["department"]
            businessline = api_req_id[flow.id]["businessline"]
            del api_req_id[flow.id]
            content_type = flow.response.headers.get("Content-Type", "").lower()
            # 提取主类型和子类型（例如：text/html; charset=utf-8 → text/html）
            if ";" in content_type:
                content_type = content_type.split(";")[0].strip()
            # 判断是否为静态文件
            if content_type in black_type:
                return
            if request.method in black_methods:
                return
            if flow.response.status_code == 200:
                # 创建一个新线程来执行修改后的请求
                threading.Thread(target=api_collection, args=(request, flow.response, department, businessline)).start()


async def config_mitmproxy(listen_host="127.0.0.1", listen_port=8888):
    """配置 mitmproxy 参数与启动"""
    options = Options(listen_host=listen_host, listen_port=listen_port)
    script = Counter()
    addons = [script]

    # 创建 DumpMaster 实例
    master = DumpMaster(options)
    master.addons.add(*addons)
    try:
        await master.run()  # 启动 mitmproxy 主循环
    except KeyboardInterrupt:
        master.shutdown()  # 当手动中断时，关闭 master


def run_mitmproxy(listen_host: str, listen_port: int):
    """运行 mitmproxy"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(config_mitmproxy(listen_host, listen_port))
    loop.close()


def start_mitmproxy(listen_host: str, listen_port: int) -> Process:
    """启动 mitmproxy"""
    mitmproxy_process = Process(target=run_mitmproxy, args=(listen_host, listen_port,))
    mitmproxy_process.start()
    # print("Mitmproxy is running")
    logger.info("Mitmproxy is running......")
    return mitmproxy_process


def stop_mitmproxy(process: Process):
    """停止 mitmproxy"""
    if process:
        process.terminate()
        process.join()
    # print("Mitmproxy Normal Exit")
    logger.info("Mitmproxy is stop......")


if __name__ == "__main__":
    mitmproxy_process = start_mitmproxy("127.0.0.1", 8888)  # 启动 mitmproxy
    # time.sleep(30)  # 延迟30s后，关闭 mitmproxy
    # stop_mitmproxy(mitmproxy_process)  # 停止 mitmproxy
    app.run(host="127.0.0.1", port=5000)

