#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import traceback
from datetime import datetime, timedelta

from sqlalchemy import desc, func

import util.log
from app import db
from app.models import WorkOrder
from app.source.commontParams import json_response

logger = util.log.get_logger()


def workOrderSearch(data):
    # 构建查询（固定按 createdAt 字段倒序）
    query = WorkOrder.query.order_by(desc(WorkOrder.createAt))
    if 'riskName' in data and data['riskName'] != '':
        query = query.filter(WorkOrder.riskName.ilike(f'%{data["riskName"]}%'))
    if 'riskType' in data and data['riskType'] != '':
        query = query.filter(WorkOrder.riskType.ilike(f'%{data["riskType"]}%'))
    if 'riskLevel' in data and data['riskLevel'] != '':
        query = query.filter(WorkOrder.riskLevel == data['riskLevel'])
    if 'department' in data and data['department'] != '':
        query = query.filter(WorkOrder.department.ilike(f'%{data["department"]}%'))
    if 'businessline' in data and data['businessline'] != '':
        query = query.filter(WorkOrder.businessline.ilike(f'%{data["businessline"]}%'))
    if 'status' in data and data['status'] != '':
        query = query.filter(WorkOrder.status.ilike(f'%{data["status"]}%'))
    # 执行分页查询
    paginated_workOrder = query.paginate(page=data['page'], per_page=data['limit'], error_out=False)
    # 转换为 JSON 格式
    results = [{
        'id': wOrder.id,
        'riskName': wOrder.riskName,
        'riskType': wOrder.riskType,
        'riskLevel': wOrder.riskLevel,
        'department': wOrder.department,
        'businessline': wOrder.businessline,
        'currentOwner': wOrder.currentOwner,
        'status': wOrder.status,
        'createAt': wOrder.createAt.strftime('%Y-%m-%d %H:%M:%S')
    } for wOrder in paginated_workOrder.items]

    return json_response(data=results, count=paginated_workOrder.total, msg='', status=0)


def workOrderDetail(id):
    wOrder = WorkOrder.query.get(id)
    result = {
        'id': wOrder.id,
        'riskName': wOrder.riskName,
        'riskType': wOrder.riskType,
        'riskLevel': wOrder.riskLevel,
        'department': wOrder.department,
        'businessline': wOrder.businessline,
        'currentOwner': wOrder.currentOwner,
        'status': wOrder.status,
        'originalRequest': wOrder.originalRequest,
        'originalResponse': wOrder.originalResponse,
        'dastRequest': wOrder.dastRequest,
        'dastResponse': wOrder.dastResponse,
        'createAt': wOrder.createAt.strftime('%Y-%m-%d %H:%M:%S')
    }
    return json_response(data=result, count=1, msg='', status=200)


def workOrderUpdate(data):
    if not data['id']:
        return json_response([], 0, '传入数据出错', 400)

    wOrder = WorkOrder.query.get(data['id'])
    wOrder.riskName = data['riskName']
    wOrder.riskType = data['riskType']
    wOrder.riskLevel = data['riskLevel']
    wOrder.department = data['department']
    wOrder.businessline = data['businessline']
    wOrder.status = data['status']
    wOrder.currentOwner = data['currentOwner']
    try:
        db.session.commit()
        return json_response([], 0, "更新成功", 200)
    except Exception as e:
        # 发生错误时回滚
        db.session.rollback()
        traceback.print_exc()
        return json_response([], 0, '更新失败', 400)


def workOrderDel(data):
    for id in data:
        try:
            wOrder = WorkOrder.query.get_or_404(id)
            db.session.delete(wOrder)
            db.session.commit()
        except Exception as e:
            # 发生错误时回滚
            db.session.rollback()
            traceback.print_exc()
            logger.info("id = " + str(id) + " 删除失败")
    return json_response([], 0, '删除成功', 200)


def workOrderUpdateStatus(data):
    if not data['id']:
        return json_response([], 0, '传入数据出错', 400)

    wOrder = WorkOrder.query.get(data['id'])
    wOrder.status = data['status']
    try:
        db.session.commit()
        return json_response([], 0, "status更新成功", 200)
    except Exception as e:
        # 发生错误时回滚
        db.session.rollback()
        traceback.print_exc()
        return json_response([], 0, 'status更新失败', 400)


def workOrderCount():
    try:
        # 计算最近5天的日期范围（包含今天）
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=4)

        # 生成日期列表（最近5天）
        date_list = [(start_date + timedelta(days=i)).strftime('%m-%d')
                     for i in range(5)]

        # 按日期分组统计工单数量
        stats = db.session.query(
            func.date(WorkOrder.createAt).label('date'),
            func.count(WorkOrder.id).label('count')
        ).filter(
            func.date(WorkOrder.createAt) >= start_date,
            func.date(WorkOrder.createAt) <= end_date
        ).group_by('date').all()

        # 转换为字典 {日期: 数量}
        stats_dict = {
            day.strftime('%m-%d'): count
            for day, count in stats
        }

        # 确保所有日期都有数据（没有的填0）
        result = [stats_dict.get(date, 0) for date in date_list]

        return json_response({
                'dates': date_list,
                'counts': result
            }, 0, "工单数量获取成功", 200)
    except Exception as e:
        traceback.print_exc()
        return json_response([], 0, '工单数量获取失败', 400)