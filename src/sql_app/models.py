# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : models.py
# Time       ：2022/4/12 9:07 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from typing import Optional

from sqlmodel import SQLModel, Field


class Bot(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    token: Optional[str] = None


class Task(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    appDriverCode: str
    bankCode: str
    orderNo: str
    status: str
    amount: str
    payeeBankCard: str
    payee: str
    bankType: str
    payeeBankCode: str
