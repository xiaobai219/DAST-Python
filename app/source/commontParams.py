#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import make_response, jsonify

# 扫描规则
rules = []

# 接口收集规则
api_collection_rules = []


# 定义通用的 JSON 响应格式
def json_response(data, count, msg, status=200):
    return make_response(jsonify({
        'code': status,
        'count': count,
        'data': data,
        'message': msg
    }), 200)
