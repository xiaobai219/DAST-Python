#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import traceback
import uuid
from datetime import datetime

import requests
from mitmproxy.http import Request, Response
import urllib3
import util.log
from app import db, app
from app.models import scanList, WorkOrder
from util.http_diff_tool import request_to_text, response_to_text, calculate_similarity

urllib3.disable_warnings()
logger = util.log.get_logger()


def dast_scan(request: Request, response: Response, r, department, businessline):
    if not pre_check_dast_time(request):
        return
    orange_request_text = request_to_text(request)
    orange_response_text = response_to_text(response)

    method = request.method
    headers = dict(request.headers)

    rules = r["rules"]
    for key in rules:
        if key == "addHeader" or key == "changeHeader":
            for val in rules[key]:
                header = val.split(":")
                headers[header[0]] = header[1].strip()
        if key == "removeHeader":
            for val in rules[key]:
                header = val.split(":")
                headers.pop(header[0], "")

    body = request.get_content().decode("utf-8", errors="ignore")
    try:
        res = requests.request(method=method, url=request.url, headers=headers, data=body, timeout=5, verify=False)
        dast_request_text = request_to_text(request, headers)
        dast_response_text = response_to_text(response, res, request.http_version)
        number = calculate_similarity(response.get_content().decode("utf-8", errors="ignore"),
                                      res.content.decode("utf-8", errors="ignore"))
        insertScanList(res.url.split("?")[0], number)
        if number >= 0.7:
            insertWorkOrder(r, res.url.split("?")[0], department, businessline, orange_request_text, orange_response_text, dast_request_text, dast_response_text)
    except Exception as e:
        logger.error("dast扫描发起请求出错" + traceback.print_exc())


# 添加扫描记录入库
def insertScanList(scanPath: str, similarity):
    sList = scanList()
    rid_compact = str(uuid.uuid4())
    rid = rid_compact.replace('-', '')
    sList.id = rid
    if scanPath.endswith("/"):
        scanPath = scanPath[0: len(scanPath) - 1]
    sList.scanPath = scanPath
    sList.similarity = similarity
    # 获取当前时间
    now = datetime.now()
    # 格式化为字符串
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    sList.scanAt = formatted_time
    with app.app_context():
        db.session.add(sList)
        # 提交到数据库
        try:
            db.session.commit()
        except Exception as e:
            # 发生错误时回滚
            db.session.rollback()
            s_list = scanList.query.filter_by(scanPath=scanPath).first()
            s_list.similarity = similarity
            s_list.scanAt = formatted_time
            db.session.commit()


# 添加工单
def insertWorkOrder(r, url, department, businessline, orange_request, orange_response, dast_request, dast_response):
    wOrder = WorkOrder()
    rid_compact = str(uuid.uuid4())
    rid = rid_compact.replace('-', '')
    wOrder.id = rid
    wOrder.riskName = url + " 存在" + r["ruleName"] + "，" + r["ruleDescribe"]
    wOrder.riskType = r["ruleName"]
    wOrder.riskLevel = "中危"
    wOrder.department = department
    wOrder.businessline = businessline
    wOrder.currentOwner = "admin"
    wOrder.status = "待确认"
    wOrder.originalRequest = orange_request[:2500]
    wOrder.originalResponse = orange_response[:2500]
    wOrder.dastRequest = dast_request[:2500]
    wOrder.dastResponse = dast_response[:2500]
    # 获取当前时间
    now = datetime.now()
    # 格式化为字符串
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    wOrder.createAt = formatted_time
    with app.app_context():
        db.session.add(wOrder)
        # 提交到数据库
        try:
            db.session.commit()
        except Exception as e:
            # 发生错误时回滚
            db.session.rollback()
            traceback.print_exc()


# 前置判断时间间隔
def pre_check_dast_time(request: Request):
    scanPath = request.url.split("?")[0]
    if scanPath.endswith("/"):
        scanPath = scanPath[0: len(scanPath) - 1]
    with app.app_context():
        s_list = scanList.query.filter_by(scanPath=scanPath).first()
        if not s_list:
            return True
        target_time = datetime.strptime(s_list.scanAt.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        time_diff = now - target_time
        if time_diff.total_seconds() > 86400:  # 默认扫描时间间隔大于24小时
            return True
        return False