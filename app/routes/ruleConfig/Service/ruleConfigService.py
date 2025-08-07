#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
import traceback
from datetime import datetime

import util.log
from app import db
from app.models import RuleConfig
from app.source.commontParams import json_response

logger = util.log.get_logger()


def ruleConfigSearch(data):
    query = RuleConfig.query
    if 'scanHost' in data and data['scanHost'] != '':
        query = query.filter(RuleConfig.scanHost.ilike(f'%{data["scanHost"]}%'))
    if 'department' in data and data['department'] != '':
        query = query.filter(RuleConfig.department.ilike(f'%{data["department"]}%'))
    if 'businessline' in data and data['businessline'] != '':
        query = query.filter(RuleConfig.businessline.ilike(f'%{data["businessline"]}%'))
    # 执行分页查询
    paginated_ruleConfig = query.paginate(page=data['page'], per_page=data['limit'], error_out=False)
    # 转换为 JSON 格式
    results = [{
        'id': rConfig.id,
        'scanHost': rConfig.scanHost,
        'scanRule': rConfig.scanRule,
        'department': rConfig.department,
        'businessline': rConfig.businessline,
        'createOwner': rConfig.createOwner,
        'updateOwner': rConfig.updateOwner,
        'createAt': rConfig.createAt.strftime('%Y-%m-%d %H:%M:%S')
    } for rConfig in paginated_ruleConfig.items]

    return json_response(data=results, count=paginated_ruleConfig.total, msg='', status=0)


def ruleConfigDel(data):
    for id in data:
        try:
            rConfig = RuleConfig.query.get_or_404(id)
            db.session.delete(rConfig)
            db.session.commit()
        except Exception as e:
            # 发生错误时回滚
            db.session.rollback()
            traceback.print_exc()
            logger.info("id = " + str(id) + " 删除失败")
    return json_response([], 0, '删除成功', 200)


def ruleConfigAdd(data):
    rConfig = None
    if data['id']:
        rConfig = RuleConfig.query.get(data['id'])
    else:
        rConfig = RuleConfig()
    rConfig.scanHost = data['host']
    rConfig.scanRule = json.dumps(data['rules'], ensure_ascii=False)
    rConfig.department = data['department']
    rConfig.businessline = data['businessline']
    rConfig.createOwner = data['createOwner']
    rConfig.updateOwner = rConfig.createOwner
    # 获取当前时间
    now = datetime.now()
    # 格式化为字符串
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    rConfig.createAt = formatted_time
    # 提交到数据库
    try:
        message = ''
        if not data['id']:
            db.session.add(rConfig)
            message = '新增成功'
        else:
            message = '更新成功'
        db.session.commit()
        return json_response([], 0, message, 200)
    except Exception as e:
        # 发生错误时回滚
        db.session.rollback()
        traceback.print_exc()
        return json_response([], 0, '新增失败,Host可能已经存在', 400)


def ruleConfigGet(id):
    rConfig = RuleConfig.query.get(id)
    result = {
        'id': rConfig.id,
        'scanHost': rConfig.scanHost,
        'scanRule': rConfig.scanRule,
        'department': rConfig.department,
        'businessline': rConfig.businessline,
        'createOwner': rConfig.createOwner,
        'updateOwner': rConfig.updateOwner,
        'createAt': rConfig.createAt.strftime('%Y-%m-%d %H:%M:%S')
    }
    return json_response(data=result, count=1, msg='', status=200)