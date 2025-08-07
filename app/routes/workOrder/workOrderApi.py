#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import Blueprint, request
from app.routes.workOrder.service import workOrderService
from app.source.commontParams import json_response

workOrder_bp = Blueprint('workOrder', __name__)


@workOrder_bp.route('/api/searchWorkOrder', methods=["POST"])
def workOrderSearch():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return workOrderService.workOrderSearch(data)


@workOrder_bp.route('/api/workOrder/deleteById', methods=["POST"])
def workOrderDel():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return workOrderService.workOrderDel(data)


@workOrder_bp.route('/api/workOrder/detail', methods=['GET'])
def workOrderDetail():
    id = request.args.get('id')
    if not id:
        return json_response([], 0,'传入数据出错', 400)

    return workOrderService.workOrderDetail(id)


@workOrder_bp.route('/api/workOrder/update', methods=['POST'])
def workOrderUpdate():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return workOrderService.workOrderUpdate(data)


@workOrder_bp.route('/api/workOrder/updateStatus', methods=['POST'])
def workOrderUpdateStatus():
    data = request.get_json()
    if not data:
        return json_response([], 0, '传入数据出错', 400)

    return workOrderService.workOrderUpdateStatus(data)


@workOrder_bp.route('/api/workOrder/count', methods=['GET'])
def workOrderCount():
    return workOrderService.workOrderCount()