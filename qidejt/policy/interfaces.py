# -*- coding: UTF-8 -*-
from qidejt.policy import _
from zope import schema
from zope.interface import Interface


class InputError(Exception):
    """Exception raised if there is an error making a data input
    """

# 文件夹mark interfaces,用于定义视图
# todo :定义db_ajax_listing view


class IContainerTablelist (Interface):
    """文件夹标记接口"""
