#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import Blueprint, request
from app.routes.ruleConfig.Service import ruleConfigService
from app.source.commontFunc import init_rules
from app.source.commontParams import json_response

ruleConfig_bp = Blueprint('ruleConfig', __name__)


@ruleConfig_bp.route('/api/searchRuleConfig', methods=["POST"])
def ruleConfigSearch():
    data = request.get_json()
    if not data:
        return json_response([], 0,'传入数据出错', 400)

    return ruleConfigService.ruleConfigSearch(data)


@ruleConfig_bp.route('/api/ruleConfig/deleteById', methods=["POST"])
def ruleConfigDel():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return ruleConfigService.ruleConfigDel(data)


@ruleConfig_bp.route('/api/ruleConfig/add', methods=["POST"])
def ruleConfigAdd():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return ruleConfigService.ruleConfigAdd(data)


@ruleConfig_bp.route('/api/ruleConfig/get', methods=["GET"])
def ruleConfigGet():
    id = request.args.get("id")
    if not id:
        return json_response([], 0, '传入数据出错', 400)

    return ruleConfigService.ruleConfigGet(id)


@ruleConfig_bp.route('/api/ruleConfig/apply', methods=['GET'])
def ruleConfigApply():
    return init_rules()