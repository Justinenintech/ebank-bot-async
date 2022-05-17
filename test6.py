# # # # !/usr/bin/env python
# # # # -*-coding:utf-8 -*-
# # #
# # # """
# # # # File       : test6.py
# # # # Time       ：2022/5/1 6:04 下午
# # # # Author     ：Eagle
# # # # version    ：python 3.8
# # # # Description：
# # # """
# # # # from decimal import *
# # # # print(int(Decimal('50.005679').quantize(Decimal('0'))))
# # # # print(type(round(50.005679)))
# # # import ast
# # # import json
# # #
# # # from src.base.async_http import MySession
# # import asyncio
# # import json
# #
# # from src.constructor.request_constructor import LoginResult
# # from src.service.bot_task_service import BaseService
# #
# # _bs = BaseService()
# # # _login_failed_result = LoginResult()
# # # print(_login_failed_result.__dict__)
# # # print('type',type(_login_failed_result.__dict__))
# # # _login_failed_result = LoginResult()
# #
# # async def hd():
# #     _login_failed_result = LoginResult()
# #     # print('_login_failed_result',_login_failed_result)
# #     # print('tupe',type(_login_failed_result))
# #     # d_param = json.dumps(_login_failed_result.__dict__)
# #     # l_param = json.loads(d_param)
# #     # print('param',json.loads(d_param))
# #     # result = json.dumps(_login_failed_result)
# #     # print('result',result)
# #     # jd = {'payeeCard': 'None', 'status': 'Failure', 'bankTradeNo': 'None', 'balance': 'None', 'errMsg': 'None', 'base64ImageCaptcha': 'None', 'showSecLoginCode': 'N', 'isBase64Image': 'N'}
# #     # jd ={'status': 'Failure'}
# #     await _bs.push_login_result(_login_failed_result,'3040442915345555459')
# #
# # loop = asyncio.new_event_loop()
# # asyncio.set_event_loop(loop)
# # loop.run_until_complete(hd())
# # # param = MySession.convert_data(_login_failed_result)
# # # print('_login_failed_result', type(_login_failed_result))
# # # print('param', param)
# # # print('param', type(param))
# # #
# # # print('ddddd',json.loads(param))
#
# # # print('ddddd',type(json.loads(param)))
# import asyncio
#
# from src.constructor.request_constructor import PayResult
# from src.enum.mb_bank_enum import MBElementEnum
# from src.enum.resp_code_enum import ResponseCode
# from src.service.bot_task_service import BaseService
# from src.sql_app.crud import get_task_by_id
#
# # print(MBElementEnum.CAPTCHA.value[0])
# # print(MBElementEnum.TRANSFER_BANK_SELECT.value[0])
# # str2 = '.form-group:nth-child(6) .form-control'
# # str1 = 'document.querySelector("%s").value=""' % str2
# # print(str1)
# # get_task_by_id()
import asyncio

from src.constructor.request_constructor import PayResult, LoginResult
from src.enum.resp_code_enum import ResponseCode
from src.service.bot_task_service import BaseService


async def hd():
    bs = BaseService()
    status = ResponseCode.Failed.value
    summary = "登录超时或支付超时,支付失败"
    pay_result = PayResult(payer='9901740669', status=status,
                           bank_trade_no='3052224422955343872',
                           summary=summary)
    _msg = "登录超时或支付超时，支付失败!"
    login_failed_result = LoginResult(errMsg="获取登录信息超时，登录失败!")
    # self.push_login_result(login_failed_result.__dict__, task_id)
    # pay_result = PayResult(summary=_msg)

    # await bs.push_otp_intermediate_result(pay_result, '3050747246263296003')
    print('pay_result',pay_result.__dict__)
    # await bs.push_otp_intermediate_result(pay_result, '3051970624747888647')
    await bs.push_pay_result(pay_result, '3052224422955343875')
    # await bs.push_login_result(login_failed_result,'3052197484920463363')
    # _login_failed_result = LoginResult()
    # # print('_login_failed_result',_login_failed_result)
    # # print('tupe',type(_login_failed_result))
    # # d_param = json.dumps(_login_failed_result.__dict__)
    # # l_param = json.loads(d_param)
    # # print('param',json.loads(d_param))
    # # result = json.dumps(_login_failed_result)
    # # print('result',result)
    # # jd = {'payeeCard': 'None', 'status': 'Failure', 'bankTradeNo': 'None', 'balance': 'None', 'errMsg': 'None', 'base64ImageCaptcha': 'None', 'showSecLoginCode': 'N', 'isBase64Image': 'N'}
    # # jd ={'status': 'Failure'}
    # await _bs.push_login_result(_login_failed_result,'3040442915345555459')
#
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(hd())
