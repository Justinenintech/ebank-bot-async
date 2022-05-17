# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : create_db.py
# Time       ：2022/4/12 9:27 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from sqlmodel import SQLModel

from .database import engine

# print("CREATING DATABASE........")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
