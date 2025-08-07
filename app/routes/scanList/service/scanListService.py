#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from sqlalchemy import desc

from app.models import scanList
from app.source.commontParams import json_response


def scanListSearch(data):
    query = scanList.query.order_by(desc(scanList.scanAt))
    if 'id' in data and data['id'] != '':
        query = query.filter(scanList.id == data['id'])
    if 'scanPath' in data and data['scanPath'] != '':
        query = query.filter(scanList.scanPath.ilike(f'%{data["scanPath"]}%'))
    # 执行分页查询
    paginated_scanList = query.paginate(page=data['page'], per_page=data['limit'], error_out=False)
    # 转换为 JSON 格式
    results = [{
        'id': sList.id,
        'scanPath': sList.scanPath,
        'similarity': sList.similarity,
        'scanAt': sList.scanAt.strftime('%Y-%m-%d %H:%M:%S')
    } for sList in paginated_scanList.items]

    return json_response(data=results, count=paginated_scanList.total, msg='', status=0)