#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.source import commontParams

app = Flask(__name__)
# app.config.from_object('config.Config')
# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/dast_data'
app.config['SQLALCHEMY_POOL_SIZE'] = 10  # 连接池大小
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20  # 最大溢出连接数
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30  # 连接超时时间
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600  # 连接回收时间

db = SQLAlchemy()  # 先初始化 db 对象，不绑定 app


def create_app():
    # 关键：在 db 初始化后导入路由
    db.init_app(app)

    from app.routes import view
    from app.routes.common import commonApi
    from app.routes.workOrder import workOrderApi
    from app.routes.asset import assetApi
    from app.routes.api import apiApi
    from app.routes.ruleConfig import ruleConfigApi
    from app.routes.scanList import scanListApi

    app.register_blueprint(view.view_bp)
    app.register_blueprint(commonApi.common_bp)
    app.register_blueprint(workOrderApi.workOrder_bp)
    app.register_blueprint(assetApi.asset_bp)
    app.register_blueprint(apiApi.api_bp)
    app.register_blueprint(ruleConfigApi.ruleConfig_bp)
    app.register_blueprint(scanListApi.scanList_bp)

    # 在应用上下文内创建表
    with app.app_context():
        # 初始化扫描规则
        from app.models import RuleConfig
        from app.models import Asset
        query = RuleConfig.query
        result = query.all()
        commontParams.rules = [{rConfig.scanHost: json.loads(rConfig.scanRule), "department": rConfig.department, "businessline": rConfig.businessline} for rConfig in result]
        asset_query = Asset.query
        result = asset_query.all()
        commontParams.api_collection_rules = [{"url": asset.url, "department": asset.department, "businessline": asset.businessline} for asset in result]

    return app

