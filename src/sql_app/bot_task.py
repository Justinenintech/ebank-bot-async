# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : bot_task.py
# Time       ：2022/4/12 9:33 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import json
import traceback
from typing import List

from fastapi import FastAPI, status, Query
# from fastapi.responses import ORJSONResponse
from starlette.responses import JSONResponse

from . import crud, schemas
from .create_db import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.get("/bot", status_code=status.HTTP_200_OK,
         response_class=JSONResponse)
async def read_bot():
    result = await crud.get_all_bot()
    if result is None or len(result) is 0:
        error_str = traceback.format_exc()
        res = {"code": '4004', "data": 'None', "msg": 'bot not found',
               "error": error_str}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=res)
    return JSONResponse(
        {"code": '0000', "data": result[0].json(),
         "msg": 'Records were successfully queried'})


@app.post("/bot", response_model=schemas.BotRead, status_code=status.HTTP_200_OK,
          response_class=JSONResponse)
async def create_bot(bot: schemas.BotCreate):
    bot_id = await crud.get_bot_by_id(bot.id)
    if bot_id:
        error_str = traceback.format_exc()
        res = {"code": '4000', "data": bot_id.json(),
               "msg": 'bot already registered',
               "error": error_str}
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=res)
    result = await crud.create_bot(bot)
    return JSONResponse(
        {"code": '0000', "data": result.json(),
         "msg": 'Robot registered successfully'})


@app.get("/task", response_model=schemas.TaskCreate, status_code=status.HTTP_200_OK,
         response_class=JSONResponse)
async def read_task(task: schemas.TaskSearch, skip: int = 0, limit: int = Query(default=2, lte=10)):
    result = await crud.get_where_task(task.status, skip=skip, limit=limit)
    print('result', result)
    ls = []
    for _ in result:
        print('_', _)
        ls.append(_.json())
    # json.dumps(ls)
    print('lssssssssss', ls)
    if result is None or len(result) is 0:
        error_str = traceback.format_exc()
        res = {"code": '4004', "data": result,
               "msg": 'task not found',
               "error": error_str}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=res)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"code": '0000', "data": json.dumps(ls),
                                 "msg": 'Records were successfully queried'})


@app.post("/task/create", response_model=schemas.TaskCreate, status_code=status.HTTP_200_OK,
          response_class=JSONResponse)
async def create_task(task: schemas.TaskCreate):
    task_id = await crud.get_task_by_id(task.id)
    if task_id:
        error_str = traceback.format_exc()
        res = {"code": '4000', "data": task_id.json(),
               "msg": 'task already registered',
               "error": error_str}
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=res)
    result = await crud.create_task(task)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"code": '0000', "data": result.json(),
                                 "msg": 'Task successfully inserted into cache'})


# @app.post("/task/update", response_model=schemas.TaskCreate, status_code=status.HTTP_200_OK,
#           response_class=JSONResponse)
# async def update_task(task: schemas.TaskUpdate):
#     task_id = await crud.get_task_by_id(task.id)
#     if task_id is None:
#         error_str = traceback.format_exc()
#         res = {"code": '4004', "data": task_id,
#                "msg": 'task not found',
#                "error": error_str}
#         # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
#                             content=res)
#     result = await crud.update_task(task)
#     return JSONResponse(status_code=status.HTTP_200_OK,
#                         content={"code": '0000', "data": result.json(),
#                                  "msg": 'Task successfully updated into cache'})
