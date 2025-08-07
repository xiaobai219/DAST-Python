#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
import traceback

from app import app, db
from app.models import RuleConfig, Asset
from app.source import commontParams
from app.source.commontParams import json_response


# 应用黑盒扫描规则
def init_rules():
    with app.app_context():
        try:
            query = RuleConfig.query
            result = query.all()
            commontParams.rules.clear()
            commontParams.rules = [{rConfig.scanHost: json.loads(rConfig.scanRule), "department": rConfig.department,
                      "businessline": rConfig.businessline} for rConfig in result]
            return json_response([], 0, '应用规则成功', 200)
        except Exception as e:
            # 发生错误时回滚
            db.session.rollback()
            traceback.print_exc()
            return json_response([], 0, '应用规则失败', 400)


# 应用api收集规则
def init_api_collection_rules():
    with app.app_context():
        try:
            asset_query = Asset.query
            result = asset_query.all()
            commontParams.api_collection_rules.clear()
            commontParams.api_collection_rules = [
                {"url": asset.url, "department": asset.department, "businessline": asset.businessline} for asset in result]
            return json_response([], 0, '应用规则成功', 200)
        except Exception as e:
            # 发生错误时回滚
            db.session.rollback()
            traceback.print_exc()
            return json_response([], 0, '应用规则失败', 400)