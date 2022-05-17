# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : run_enum.py
# Time       ：2022/4/29 1:42 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from enum import Enum, unique


@unique
class RunEnum(Enum):
    """
    驱动任务
    """
    RUN_READY = 'Ready'
