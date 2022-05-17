# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : bot_task_service.py.py
# Time       ：2022/4/15 10:09 上午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import ast
import asyncio
import json

from loguru import logger

from setttings import SERVER_HOST, FREQUENCY_TIME, CODE, SERVICE_TYPE, SERIAL
from src.base.async_http import MySession
from src.base.tools import Tools
# from src.app.run import RunDriver
from src.enum.bot_api_enum import BotApi

from src.enum.resp_code_enum import ResponseCode
from src.enum.run_enum import RunEnum
from src.sql_app.crud import get_where_all, update_task


class BaseService:

    def __init__(self):
        # self._run = RunDriver()
        """
        配置系统默认使用数据
        """
        self._host = SERVER_HOST
        self._api = BotApi
        self._frequency_time = FREQUENCY_TIME
        self._t = Tools()
        self._register_data = {
            "code": CODE,
            "ip": self._t.get_ip(),
            "serviceType": SERVICE_TYPE,
            "serialNo": SERIAL,
            "type": 'Web'
        }

    async def register(self):
        res = await MySession.get('http://127.0.0.1:8000' + '/bot')
        if res['code'].__eq__(ResponseCode.Success.value):
            # pass
            res_data = ast.literal_eval(res['data'])
            logger.debug("已注册机器人ID：{}".format(res_data['id']))
            return res_data['id']
        else:
            res = await MySession.post(self._host + self._api.Register_Device_Url.value,
                                       data=self._register_data)
            logger.debug("bot 注册信息-{}".format(res))
            bot_id = res['data']['id']
            _id = {'id': bot_id, 'token': 'None'}
            cache = await MySession.post('http://127.0.0.1:8000' + '/bot', data=_id)
            logger.debug("bot 写入缓存-{}".format(cache))
            return None

    async def pull_task(self, bot_id):
        """
        拉取任務
        :return: 任務
        """
        url = self._host + self._api.Get_Task_Url.get_task_url(bot_id)
        task_res = await MySession.get(url)
        logger.debug(task_res)
        if task_res['code'].__eq__(ResponseCode.Success.value):
            task = {
                "id": task_res['data']['id'],
                "appDriverCode": task_res['data']['appDriverCode'],
                "bankCode": task_res['data']['bankCode'],
                "orderNo": task_res['data']['orderNo'],
                "status": task_res['data']['status'],
                "amount": task_res['data']['amount'],
                "payeeBankCard": task_res['data']['payeeBankCard'],
                "payee": task_res['data']['payee'],
                "bankType": task_res['data']['bankType'],
                "payeeBankCode": task_res['data']['payeeBankCode']
            }
            cache = await MySession.post('http://127.0.0.1:8000' + '/task/create', data=task)
            logger.debug('任务成功写入到缓存：{}'.format(cache))

    async def push_captcha_base64(self, task_id, captcha):
        """
        推送图形验证码
        :param task_id: 任务id
        :param captcha: base64Image
        """
        task = {
            "id": task_id,
            "captcha": str(captcha)
        }
        logger.debug("推送图形验证码请求参数：{}".format(task))
        url = self._host + str(self._api.Push_Captcha_Task_Url.value) \
            .replace("{taskId}", task_id)
        res = await MySession.post(url, data=task)
        logger.debug("推送图形验证码-{}".format(res))

    async def get_login_info(self, bot_id, task_id):
        """
        获取登录信息
        :param bot_id: 机器人ID
        :param task_id: 任务ID
        :return: 登录用的账号密码，验证码信息
        """
        url = self._host + self._api.Login_Info_Url.value \
            .replace("{botId}", bot_id) \
            .replace("{taskId}", task_id)
        res = await MySession.get(url)
        logger.debug("获取登录信息，响应数据-{}".format(res))
        return res

    async def push_login_result(self, data, task_id):
        """
        登录结果接口
        :param data:  结果数据
        :param task_id: 任务id
        :return:
        """
        url = self._host + str(self._api.Login_Error_Result_Url.value) \
            .replace("{taskId}", task_id)
        res = await MySession.put(url, data=data)
        logger.debug("登录请求，响应数据-{}".format(res))

    async def push_pay_result(self, data, task_id):
        """
        支付结果
        :param data: 支付请求参数：dict
        :param task_id: 任务id
        :return:
        """
        url = self._host + self._api.Pay_Result_Url.value \
            .replace("{taskId}", task_id)
        res = await MySession.put(url, data=data)
        logger.debug("支付请求，响应数据-{}".format(res))

    async def push_otp_qr_result(self, data, task_id):
        """
        推送 otp
        :param data:  OTP 数据字典
        :param task_id: 任务id
        :return:
        """
        url = self._host + self._api.Otp_Tradeno_Url.value \
            .replace("{taskId}", task_id)
        res = await MySession.put(url, data=data)
        logger.debug("推送OTP二维码请求，响应数据-{}".format(res))

    async def try_get_otp(self, task_id):
        """
        尝试获取otp
        :param countdown: OTP倒计时
        :param task_id: 任务id
        :return: otp
        """
        # 尝试获取otp
        url = self._host + self._api.Get_Otp_Url.value \
            .replace("{taskId}", task_id)
        res = await MySession.get(url)
        logger.debug("尝试获取otp，响应数据-{}".format(res))
        return res

    async def push_otp_intermediate_result(self, data, task_id):
        """
        推送opt验证结果 接口
        :param data: 结果数据
        :param task_id: 任务id
        :return:
        """
        url = self._host + self._api.Otp_Intermediate_State.value \
            .replace("{taskId}", task_id)
        res = await MySession.put(url, data=data)
        logger.debug("推送OTP验证请求，响应数据-{}".format(res))
