#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from app import db


# 工单
class WorkOrder(db.Model):
    __tablename__ = 'workorder'
    id = db.Column('rid', db.String(100), primary_key=True)
    riskName = db.Column('risk_name', db.String(100))
    riskType = db.Column('risk_type', db.String(100))
    riskLevel = db.Column('risk_level', db.String(10))
    department = db.Column('department', db.String(100))
    businessline = db.Column('businessline', db.String(100))
    currentOwner = db.Column('current_owner', db.String(100))
    status = db.Column('status', db.String(100))
    originalRequest = db.Column('original_request', db.Text)
    originalResponse = db.Column('original_response', db.Text)
    dastRequest = db.Column('dast_request', db.Text)
    dastResponse = db.Column('dast_response', db.Text)
    createAt = db.Column('create_time', db.DateTime)


# 应用资产
class Asset(db.Model):
    __tablename__ = 'asset'
    id = db.Column('id', db.Integer, primary_key=True)
    assetName = db.Column('asset_name', db.String(100))
    url = db.Column('url', db.String(100), unique=True)
    insideOroutside = db.Column('insideOroutside', db.String(20))
    linkedApiNum = db.Column('linked_api_num', db.Integer)
    department = db.Column('department', db.String(100))
    businessline = db.Column('businessline', db.String(100))
    owner = db.Column('owner', db.String(20))
    technologyStack = db.Column('technologyStack', db.String(100))
    createAt = db.Column('create_time', db.DateTime)


# 接口资产
class Api(db.Model):
    __tablename__ = 'api'
    id = db.Column('id', db.Integer, primary_key=True)
    apiPath = db.Column('api_path', db.String(200))
    describe = db.Column('describe', db.String(100))
    department = db.Column('department', db.String(100))
    businessline = db.Column('businessline', db.String(100))
    request = db.Column('request', db.Text)
    response = db.Column('response', db.Text)
    createAt = db.Column('create_time', db.DateTime)
    updateAt = db.Column('update_time', db.DateTime)


# 扫描配置
class RuleConfig(db.Model):
    __tablename__ = 'rule_config'
    id = db.Column('id', db.Integer, primary_key=True)
    scanHost = db.Column('scan_host', db.String(100), unique=True)
    scanRule = db.Column('scan_rule', db.String(10000))
    department = db.Column('department', db.String(100))
    businessline = db.Column('businessline', db.String(100))
    createOwner = db.Column('create_owner', db.String(100))
    updateOwner = db.Column('update_owner', db.String(100))
    createAt = db.Column('create_time', db.DateTime)


# 扫描列表
class scanList(db.Model):
    __tablename__ = 'scan_list'
    id = db.Column('rid', db.String(100), primary_key=True)
    scanPath = db.Column('scan_path', db.String(100), unique=True)
    similarity = db.Column('similarity', db.Integer)
    scanAt = db.Column('scan_time', db.DateTime)