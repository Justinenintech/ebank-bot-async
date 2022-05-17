# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : async_http.py
# Time       ：2022/4/9 1:21 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import json

import aiohttp
from loguru import logger


class MySession:
    _session = None

    @classmethod
    def session(cls):
        _headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        if not cls._session:
            cls._session = aiohttp.ClientSession(headers=_headers)
        return cls._session

    @classmethod
    def close(cls):
        return cls._session.close()

    @classmethod
    def convert_data(cls, data):
        """
        请求数据类型转化
        :param data: 数据
        """
        param = None
        if isinstance(data, str):
            param = data
        elif isinstance(data, dict):
            param = json.dumps(data).encode('utf-8')
        elif isinstance(data, object):
            param = json.dumps(data.__dict__).encode('utf-8')
        # logger.info("paramparamparamparam-{} ", param)
        return param

    @staticmethod
    async def post(url, data):
        # load_param = None
        param = MySession.convert_data(data)
        # if isinstance(param, bytes):
        #     load_param = json.loads(param)
        # logger.debug("load_param:{}".format(load_param))
        async with MySession.session().post(url, data=param) as r:
            data = await r.read()
            # print('data',data)
            json_body = json.loads(data)
            # print('请求相应：', json_body)
            return json_body

    @staticmethod
    async def get(url, **kwargs):
        param = MySession.convert_data(kwargs)
        async with MySession.session().get(url, data=param) as r:
            data = await r.read()
            # print('data',data)
            json_body = json.loads(data)
            # print('请求相应：', json_body)
            return json_body

    @staticmethod
    async def put(url, data):
        """

        :param url:
        :param data:
        :return:
        """
        param = MySession.convert_data(data)
        async with MySession.session().put(url, data=param) as r:
            data = await r.read()
            logger.debug('data:{}'.format(data))
            json_body = json.loads(data)
            logger.debug('请求相应:{}'.format(json_body))
            # print('请求相应：', json_body)
            return json_body

    @staticmethod
    async def close_session():
        await MySession.close()

# url = 'http://www.baidu.com'
#
#
# # async def bdad(url):
#
#
# # before start your app
# loop = asyncio.get_event_loop()
#
# loop.run_until_complete(get_sth())
# # ...
#
# # after stop your app
# loop.run_until_complete(close_session())
