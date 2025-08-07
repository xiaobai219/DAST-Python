#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import Blueprint, request

from app.routes.api.service import apiService
from app.source.commontParams import json_response

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/searchApi', methods=["POST"])
def workOrderSearch():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return apiService.apiSearch(data)


@api_bp.route('/api/api/add', methods=['POST'])
def apiAdd():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return apiService.apiAdd(data)


@api_bp.route('/api/api/deleteById', methods=['POST'])
def apiDel():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return apiService.apiDel(data)


@api_bp.route('/api/api/count', methods=['GET'])
def apiCount():
    return apiService.apiCount()


@api_bp.route('/api/api/detail', methods=['GET'])
def apiDetail():
    id = request.args.get('id')
    if not id:
        return json_response([], 0, '传入数据出错', 400)

    return apiService.apiDetail(id)