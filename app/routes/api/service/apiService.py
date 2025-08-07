#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import traceback
from datetime import datetime, timedelta

from sqlalchemy import func

import util.log
from app import db
from app.models import Api
from app.source.commontParams import json_response

logger = util.log.get_logger()


def apiSearch(data):
    query = Api.query
    if 'apiPath' in data and data['apiPath'] != '':
        query = query.filter(Api.apiPath.ilike(f'%{data["apiPath"]}%'))
    if 'department' in data and data['department'] != '':
        query = query.filter(Api.department.ilike(f'%{data["department"]}%'))
    if 'businessline' in data and data['businessline'] != '':
        query = query.filter(Api.businessline.ilike(f'%{data["businessline"]}%'))
    # 执行分页查询
    paginated_api= query.paginate(page=data['page'], per_page=data['limit'], error_out=False)
    # 转换为 JSON 格式
    results = [{
        'id': api.id,
        'apiPath': api.apiPath,
        'describe': api.describe,
        'department': api.department,
        'businessline': api.businessline,
        'createAt': api.createAt.strftime('%Y-%m-%d %H:%M:%S'),
        'updateAt': api.updateAt.strftime('%Y-%m-%d %H:%M:%S')
    } for api in paginated_api.items]

    return json_response(data=results, count=paginated_api.total, msg='', status=0)


def apiAdd(data):
    api = Api()
    api.apiPath = data['apiPath']
    api.describe = data['describe']
    api.department = data['department']
    api.businessline = data['businessline']
    api.request = ''
    api.response = ''
    # 获取当前时间
    now = datetime.now()
    # 格式化为字符串
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    api.createAt = formatted_time
    api.updateAt = formatted_time
    db.session.add(api)
    # 提交到数据库
    try:
        db.session.commit()
        return json_response([], 0, '新增成功', 200)
    except Exception as e:
        # 发生错误时回滚
        db.session.rollback()
        traceback.print_exc()
        return json_response([], 0, '新增失败', 400)


def apiDel(data):
    for id in data:
        try:
            api = Api.query.get_or_404(id)
            db.session.delete(api)
            db.session.commit()
        except Exception as e:
            # 发生错误时回滚
            db.session.rollback()
            traceback.print_exc()
            logger.info("id = "+str(id)+" 删除失败")
    return json_response([], 0, '删除成功', 200)


def apiCount():
    try:
        # 计算最近5天的日期范围
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=4)

        # 生成日期列表
        date_list = [(start_date + timedelta(days=i)).strftime('%m-%d')
                     for i in range(5)]

        # 按日期分组统计扫描接口总数
        stats = db.session.query(
            func.date(Api.updateAt).label('date'),
            func.count(Api.id).label('count')
        ).filter(
            func.date(Api.updateAt) >= start_date,
            func.date(Api.updateAt) <= end_date
        ).group_by('date').all()

        # 转换为字典 {日期: 总数}
        stats_dict = {
            day.strftime('%m-%d'): total
            for day, total in stats
        }

        # 确保所有日期都有数据
        result = [stats_dict.get(date, 0) for date in date_list]

        return json_response({
                'dates': date_list,
                'counts': result
            }, 0, "API数量获取成功", 200)
    except Exception as e:
        traceback.print_exc()
        return json_response([], 0, 'API数量获取失败', 400)


def apiDetail(id):
    api = Api.query.get(id)
    result = {
        'id': api.id,
        'apiPath': api.apiPath,
        'describe': api.describe,
        'department': api.department,
        'businessline': api.businessline,
        'request': api.request,
        'response': api.response,
        'createAt': api.createAt.strftime('%Y-%m-%d %H:%M:%S'),
        'updateAt': api.updateAt.strftime('%Y-%m-%d %H:%M:%S'),
    }
    return json_response(data=result, count=1, msg='', status=200)