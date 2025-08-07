#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime

from mitmproxy.http import Request, Response

from app import app, db
from app.models import Api
from util.http_diff_tool import request_to_text, response_to_text


def api_collection(request: Request, response: Response, department, businessline):
    if not pre_check_collection_time(request):
        return

    api_path = request.url.split("?")[0]
    if api_path.endswith("/"):
        api_path = api_path[0: len(api_path) - 1]
    orange_request_text = request_to_text(request)
    orange_response_text = response_to_text(response)
    api = Api()
    api.apiPath = api_path
    api.describe = ''
    api.department = department
    api.businessline = businessline
    api.request = orange_request_text
    api.response = orange_response_text
    # 获取当前时间
    now = datetime.now()
    # 格式化为字符串
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    api.createAt = formatted_time
    api.updateAt = formatted_time
    with app.app_context():
        db.session.add(api)
        # 提交到数据库
        try:
            db.session.commit()
        except Exception as e:
            # 发生错误时回滚
            db.session.rollback()
            api = Api.query.filter_by(apiPath=api_path).first()
            api.request = orange_request_text[:2500]
            api.response = orange_response_text[:2500]
            api.department = department
            api.businessline = businessline
            api.updateAt = formatted_time
            db.session.commit()


def pre_check_collection_time(request: Request):
    apiPath = request.url.split("?")[0]
    if apiPath.endswith("/"):
        apiPath = apiPath[0: len(apiPath) - 1]
    with app.app_context():
        api = Api.query.filter_by(apiPath=apiPath).first()
        if not api:
            return True
        target_time = datetime.strptime(api.updateAt.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        time_diff = now - target_time
        if time_diff.total_seconds() > 86400:  # 默认扫描时间间隔大于24小时
            return True
        return False