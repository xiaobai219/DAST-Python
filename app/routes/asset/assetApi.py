#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import Blueprint, request
from app.routes.asset.service import assetService
from app.source.commontFunc import init_api_collection_rules
from app.source.commontParams import json_response

asset_bp = Blueprint('asset', __name__)


@asset_bp.route('/api/searchAsset', methods=["POST"])
def assetSearch():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return assetService.assetSearch(data)


@asset_bp.route('/api/asset/add', methods=["POST"])
def assetAdd():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return assetService.assetAdd(data)


@asset_bp.route('/api/asset/deleteById', methods=["POST"])
def assetDel():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return assetService.assetDel(data)


@asset_bp.route('/api/asset/updateNumById', methods=['POST'])
def linkedApiNumUpdate():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return assetService.linkedApiNumUpdate(data)


@asset_bp.route('/api/assetApi/count', methods=['GET'])
def assetApiCount():
    return assetService.assetApiCount()


@asset_bp.route('/api/collection/apply', methods=['GET'])
def apiCollectionApply():
    return init_api_collection_rules()


@asset_bp.route('/api/asset/get', methods=['GET'])
def assetGet():
    id = request.args.get('id')
    if not id:
        return json_response([], 0, '传入数据出错', 400)

    return assetService.assetGet(id)

