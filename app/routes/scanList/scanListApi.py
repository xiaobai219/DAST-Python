#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import Blueprint, request
from app.routes.scanList.service import scanListService
from app.source.commontParams import json_response

scanList_bp = Blueprint('scanList', __name__)


@scanList_bp.route('/api/searchScanList', methods=["POST"])
def scanListSearch():
    data = request.get_json()
    if not data:
        return json_response([], 0,'传入数据出错', 400)

    return scanListService.scanListSearch(data)