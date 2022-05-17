# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : schemas.py
# Time       ：2022/4/12 10:01 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from typing import Optional, Any

from sqlmodel import SQLModel


class BotCreate(SQLModel):
    id: str
    token: Optional[str] = None


class BotRead(BotCreate):
    pass


class TaskCreate(SQLModel):
    id: str
    appDriverCode: str
    bankCode: str
    orderNo: str
    status: str
    amount: str
    payeeBankCard: str
    payee: str
    bankType: str
    payeeBankCode: str


class TaskSearch(SQLModel):
    status: str


class TaskUpdate(SQLModel):
    id: str
    status: str