# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : crud.py
# Time       ：2022/4/12 10:07 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from fastapi import Query
from sqlmodel import Session, select
from . import models, schemas
from .database import engine
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

session = Session(bind=engine)


async def get_all_bot():
    return session.exec(select(models.Bot)).all()


async def get_bot_by_id(bot_id: str):
    return session.exec(select(models.Bot).where(models.Bot.id == bot_id)).first()


async def create_bot(bot: schemas.BotCreate):
    statement = models.Bot.from_orm(bot)
    # print('statement', statement)
    session.add(statement)
    session.commit()
    session.refresh(statement)
    return statement


async def get_where_task(status: str, skip: int = 0, limit: int = Query(default=5, lte=10)):
    return session.exec(
        select(models.Task).where(models.Task.status == status).offset(skip).limit(limit)).all()


async def get_task_by_id(task_id: str):
    return session.exec(select(models.Task).where(models.Task.id == task_id)).first()


async def get_where_all(status: str):
    return session.exec(
        select(models.Task).where(models.Task.status == status)).all()


async def create_task(task: schemas.TaskCreate):
    statement = models.Task.from_orm(task)
    # print('statement', statement)
    session.add(statement)
    session.commit()
    session.refresh(statement)
    return statement


async def update_task(task_id,status):
    select_one = select(models.Task).where(models.Task.id == task_id)
    statement = session.exec(select_one)
    up = statement.one()
    # task.status
    # statement = models.Task.from_orm(task)
    up.status = status
    # up.status = task.status
    session.add(up)
    session.commit()
    session.refresh(up)
    return up

# async def update_task(task: schemas.TaskUpdate):
#     select_one = select(models.Task).where(models.Task.id == task.id)
#     statement = session.exec(select_one)
#     up = statement.one()
#     # task.status
#     # statement = models.Task.from_orm(task)
#     up.status = task.status
#     # up.status = task.status
#     session.add(up)
#     session.commit()
#     session.refresh(up)
#     return up

# def create_user_item(task: schemas.TaskCreate, user_id: int):
#     db_item = models.Item(**task.dict(), owner_id=user_id)
#     db_item.save()
#     return db_item

# @app.put("/task/", response_model=TaskCreate)
# async def update_task(task: TaskUpdate):
#     with Session(engine) as session:
#         # db_task = Task.from_orm(task)
#         sel = select(Task).where(Task.id == task.id)
#         results = session.exec(sel)
#         res = results.one()
#         res.status = task.status
#         session.add(res)
#         session.commit()
#         session.refresh(res)
#         return res
