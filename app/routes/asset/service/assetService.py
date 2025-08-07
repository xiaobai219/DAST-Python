#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import traceback
from datetime import datetime
import util.log
from app import db
from app.models import Asset, Api
from app.source.commontParams import json_response

logger = util.log.get_logger()


def assetSearch(data):
    query = Asset.query
    if 'assetName' in data and data['assetName'] != '':
        query = query.filter(Asset.riskName.ilike(f'%{data["assetName"]}%'))
    if 'url' in data and data['url'] != '':
        query = query.filter(Asset.url.ilike(f'%{data["url"]}%'))
    if 'department' in data and data['department'] != '':
        query = query.filter(Asset.department.ilike(f'%{data["department"]}%'))
    if 'businessline' in data and data['businessline'] != '':
        query = query.filter(Asset.businessline.ilike(f'%{data["businessline"]}%'))
    if 'technologyStack' in data and data['technologyStack'] != '':
        query = query.filter(Asset.technologyStack.ilike(f'%{data["technologyStack"]}%'))
    if 'insideOroutside' in data and data['insideOroutside'] != '':
        query = query.filter(Asset.insideOroutside.ilike(f'%{data["insideOroutside"]}%'))

    # 执行分页查询
    paginated_asset = query.paginate(page=data['page'], per_page=data['limit'], error_out=False)
    # 转换为 JSON 格式
    results = [{
        'id': asset.id,
        'assetName': asset.assetName,
        'url': asset.url,
        'insideOroutside': asset.insideOroutside,
        'linkedApiNum': asset.linkedApiNum,
        'department': asset.department,
        'businessline': asset.businessline,
        'owner': asset.owner,
        'technologyStack': asset.technologyStack,
        'createAt': asset.createAt.strftime('%Y-%m-%d %H:%M:%S')
    } for asset in paginated_asset.items]

    return json_response(data=results, count=paginated_asset.total, msg='', status=0)


def assetAdd(data):
    asset = None
    if data['id']:
        asset = Asset.query.get(data['id'])
    else:
        asset = Asset()
    asset.url = data['url']
    asset.assetName = data['assetName']
    asset.department = data['department']
    asset.businessline = data['businessline']
    asset.insideOroutside = data['insideOroutside']
    asset.technologyStack = data['technologyStack']
    asset.owner = data['owner']
    # 获取当前时间
    now = datetime.now()
    # 格式化为字符串
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    asset.createAt = formatted_time
    try:
        message = ''
        if not data['id']:
            db.session.add(asset)
            message = '新增成功'
        else:
            message = '更新成功'
        db.session.commit()
        return json_response([], 0, message, 200)
    except Exception as e:
        # 发生错误时回滚
        db.session.rollback()
        traceback.print_exc()
        return json_response([], 0, '新增/更新失败，url可能已经存在', 400)


def assetDel(data):
    for id in data:
        try:
            asset = Asset.query.get_or_404(id)
            db.session.delete(asset)
            db.session.commit()
        except Exception as e:
            # 发生错误时回滚
            db.session.rollback()
            traceback.print_exc()
            logger.info("id = "+str(id)+" 删除失败")
    return json_response([], 0, '删除成功', 200)


def linkedApiNumUpdate(data):
    for id in data:
        try:
            asset = Asset.query.get_or_404(id)
            count = Api.query.filter(
                Api.apiPath.startswith(asset.url)
            ).count()
            asset.linkedApiNum = count
            db.session.commit()
        except Exception as e:
            # 发生错误时回滚
            db.session.rollback()
            traceback.print_exc()
            logger.info("id = "+str(id)+" 更新失败")
    return json_response([], 0, '更新成功', 200)


def assetApiCount():
    asset_count = Asset.query.count()
    api_count = Api.query.count()
    result = {
        "asset_count": asset_count,
        "api_count": api_count
    }
    return json_response(data=result, count=api_count + asset_count, msg='', status=200)


def assetGet(id):
    asset = Asset.query.get(id)
    result = {
        "assetName": asset.assetName,
        "url": asset.url,
        "insideOroutside": asset.insideOroutside,
        "department": asset.department,
        "businessline": asset.businessline,
        "owner": asset.owner,
        "technologyStack": asset.technologyStack
    }
    return json_response(data=result, count=1, msg='', status=200)