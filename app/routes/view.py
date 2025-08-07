#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template

view_bp = Blueprint('view', __name__)


@view_bp.route('/login')
def home():
    return render_template('login.html')


@view_bp.route('/')
def index():
    return render_template('index.html')


@view_bp.route('/view/console/console1.html')
def console():
    return render_template('view/console/console1.html')


@view_bp.route('/view/component/workOrder.html')
def workOrder():
    return render_template('view/component/workOrder.html')


@view_bp.route('/view/component/applicationAssets.html')
def appAsset():
    return render_template('view/component/applicationAssets.html')


@view_bp.route('/view/module/addAsset.html')
def addAsset():
    return render_template('view/module/addAsset.html')


@view_bp.route('/view/component/apiList.html')
def api():
    return render_template('view/component/apiList.html')


@view_bp.route('/view/module/addApi.html')
def addApi():
    return render_template('view/module/addApi.html')


@view_bp.route('/view/component/ruleConfig.html')
def scanConfig():
    return render_template('view/component/ruleConfig.html')


@view_bp.route('/view/module/addRuleConfig.html')
def addScanConfig():
    return render_template('view/module/addRuleConfig.html')


@view_bp.route('/view/component/scanList.html')
def scanList():
    return render_template('view/component/scanList.html')


@view_bp.route('/view/workOrder/detail')
def workOrderDetail():
    return render_template('view/console/detail.html')


@view_bp.route('/view/api/api_detail')
def apiDetail():
    return render_template('view/console/apiDetail.html')