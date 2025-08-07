#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from mitmproxy.http import Request, Response
import difflib
import json


def request_to_text(request: Request, headers=None):
    # 将requests转换为原始HTTP请求文本
    request_data = ""
    if headers is None:
        method = request.method
        request_line = f"{method} {request.path} {request.http_version}"
        request_headers = dict(request.headers)
        request_body = request.get_content().decode("utf-8", errors="ignore")
        headers_text = '\n'.join([f"{k}: {v}" for k, v in request_headers.items()])
        request_data = f"{request_line}\n{headers_text}\n\n{request_body}"
    elif headers is not None:
        method = request.method
        request_line = f"{method} {request.path} {request.http_version}"
        request_headers = headers
        request_body = request.get_content().decode("utf-8", errors="ignore")
        headers_text = '\n'.join([f"{k}: {v}" for k, v in request_headers.items()])
        request_data = f"{request_line}\n{headers_text}\n\n{request_body}"
    return request_data


def response_to_text(response: Response, res=None, http_version=None):
    # 将response请求转换为原始HTTP请求文本
    response_data = ""
    if http_version is None:
        response_line = f"{response.http_version} {response.status_code} {response.reason}"
        response_headers = dict(response.headers)
        response_body = response.get_content().decode("utf-8", errors="ignore")
        headers_text = '\n'.join([f"{k}: {v}" for k, v in response_headers.items()])
        response_data = f"{response_line}\n{headers_text}\n\n{response_body}"
    elif http_version is not None:
        response_line = f"{http_version} {res.status_code} {res.reason}"
        headers_text = '\n'.join([f"{k}: {v}" for k, v in res.headers.items()])
        response_body = res.content.decode("utf-8", errors="ignore")
        response_data = f"{response_line}\n{headers_text}\n\n{response_body}"
    return response_data


def calculate_similarity(text1: str, text2: str) -> float:
    # 计算两个文本的相似度
    # 尝试JSON解析(针对JSON响应)
    try:
        json1 = json.loads(text1)
        json2 = json.loads(text2)
        # 转换为规范化的JSON字符串进行比较
        text1 = json.dumps(json1, sort_keys=True)
        text2 = json.dumps(json2, sort_keys=True)
    except (json.JSONDecodeError, TypeError):
        # 不是有效的JSON，继续使用原始文本
        pass

    # 使用difflib计算相似度
    return difflib.SequenceMatcher(None, text1, text2).ratio()
