# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : mb_app.py
# Time       ：2022/4/13 2:45 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import asyncio
import functools
import time
from time import sleep

from loguru import logger

from src.driver.base_driver import BaseDriver
from src.base.tools import Tools
from src.constructor.request_constructor import LoginResult, PayResult
from src.driver.mb_driver import MBDriver
from src.enum.mb_bank_enum import MBElementEnum
# from pyquery import PyQuery as pq
from src.enum.resp_code_enum import ResponseCode
from src.service.bot_task_service import BaseService

# 工具类
from src.sql_app.crud import update_task


class Tracer:
    def __init__(self, num=None, callback=None):  # 可支持任意参数
        self.num = num
        self._bs = BaseService()
        self._callback = callback

    def __call__(self, func):
        # def run_benchmark(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            res = await func(*args, **kwargs)
            print(f'{func.__name__} run {args}  {round(time.perf_counter() - start_time)}')
            if int(self.num) >= round(time.perf_counter() - start_time):
                print('未超时')
            else:
                # await callback()
                if self._callback.__eq__('获取OTP信息超时，支付失败!'):
                    # await self.after_otp_timeout()
                    await MBApp.after_otp_timeout()
                if self._callback.__eq__('登录超时或支付超时，支付失败!'):
                    # await self.after_transfer_timeout()
                    await MBApp.after_transfer_timeout()
            return res

        return wrapper


class MBApp:
    """
    MB业务
    """

    def __init__(self, bot_id, task_id, payeeBankCode,
                 payeeBankCard, payee, amount, orderNo):
        global g_task_id
        self._bs = BaseService()
        self._bd = BaseDriver()
        self._mbd = MBDriver()
        self._bot_id = bot_id
        self._task_id = task_id
        self._payeeBankCode = payeeBankCode
        self._payeeBankCard = payeeBankCard
        self._payee = payee
        self._amount = amount
        self._orderNo = orderNo
        g_task_id = self._task_id

    @staticmethod
    async def after_otp_timeout():
        bs = BaseService()
        logger.debug('获取OTP信息超时，支付失败!')
        _msg = "获取OTP信息超时，支付失败!"
        pay_failed_result = PayResult(summary=_msg)
        # 推送otp验证结果x
        await bs.push_otp_intermediate_result(pay_failed_result, g_task_id)
        # 提交支付结果
        await bs.push_pay_result(pay_failed_result, g_task_id)

    @staticmethod
    async def after_transfer_timeout():
        bs = BaseService()
        logger.debug('登录超时或支付超时，支付失败!')
        _msg = "登录超时或支付超时，支付失败!"
        pay_failed_result = PayResult(summary=_msg)
        # 推送otp验证结果x
        logger.debug("g_task_id:{}".format(g_task_id))

        await bs.push_otp_intermediate_result(pay_failed_result, g_task_id)
        # 提交支付结果
        await bs.push_pay_result(pay_failed_result, g_task_id)

    # @_t.set_timeout(120, after_otp_timeout)
    @Tracer(num=110, callback='获取OTP信息超时，支付失败!')
    async def mb_try_get_otp(self, task_id):
        count = 1
        while count <= 110:
            print('sleep_time', count)
            res = await self._bs.try_get_otp(task_id)
            if res['data'] != None:
                return res['data']
            if res['data'] is None:
                return None
            sleep(1)
            count += 1

    async def assert_transfer_success(self, task_id):
        logger.debug(">>>>>支付成功，推送消息!<<<<<<")
        self.status = ResponseCode.Ok.value
        self.summary = "支付成功"
        pay_result = PayResult(payer=self._payeeBankCard, status=self.status,
                               bank_trade_no=self._orderNo,
                               summary=self.summary)
        # 推送otp验证结果x
        await self._bs.push_otp_intermediate_result(pay_result, task_id)
        # 提交支付结果
        await self._bs.push_pay_result(pay_result, task_id)

    async def assert_transfer_otp(self, page, task_id):
        await self._mbd.close_top_err(page)
        await self._mbd.transfer_send_otp(page)
        self.status = ResponseCode.OTP_ERROR.value
        self.summary = "第一次otp码错误, 支付失败"
        # 构造支付结果数据
        _result = PayResult(payer=self._payeeBankCode, status=self.status,
                            bank_trade_no=self._orderNo, summary=self.summary)
        logger.info('第一次otp码错误，支付失败:{}'.format(_result.__dict__))
        otp_base64 = await self._mbd.transfer_get_otp_base64(page)
        logger.debug("获取的OTP二维码为：{}".format(otp_base64.__dict__))
        # 推送OTP验证结果
        await self._bs.push_otp_intermediate_result(_result, task_id)
        # 推送OTP
        await self._bs.push_otp_qr_result(otp_base64, task_id)

        # 获取OTP
        otp = await self.mb_try_get_otp(task_id)
        # 输入OTP
        await self._mbd.transfer_input_otp(page, otp)
        # 提交转账交易
        await self._mbd.transfer_submit_otp(page)

        is_check_otp, msg = await self._mbd.check_otp_err(page)
        logger.debug("第二次检测是否出现OTP错误弹出框:{}".format(is_check_otp))
        if is_check_otp:
            await self._bd.reload_page(page)
            result_failed = LoginResult(errMsg=msg)
            await self._bs.push_login_result(result_failed, task_id)
            # 更新支付结果信息，为Failure_otp
            self.status = ResponseCode.FAILED_OTP.value
            self.summary = "第2次otp码错误，支付失败"
            pay_result = PayResult(payer=self._payeeBankCard, status=self.status,
                                   bank_trade_no=self._orderNo,
                                   summary=self.summary)
            return pay_result
        else:
            logger.debug(">>>>>OTP错误之后，进入支付成功，推送消息!<<<<<<{}".format(is_check_otp))
            self.status = ResponseCode.Ok.value
            self.summary = "第 2 次otp正确，支付成功"
            pay_result = PayResult(payer=self._payeeBankCard, status=self.status,
                                   bank_trade_no=self._orderNo,
                                   summary=self.summary)
            logger.info("\n >>> 第 {} 次支付成功: {}\n", self.summary, pay_result.__dict__)
            return pay_result

    # @_t.set_timeout(10, after_transfer_timeout)
    @Tracer(num=260, callback='登录超时或支付超时，支付失败!')
    async def transfer_app(self, browser, page, bot_id, task_id, payeeBankCode,
                           payeeBankCard, payee, amount, orderNo):

        captcha_base64 = await self._mbd.get_captcha_base64(page)
        logger.debug("获取到的验证码为：{}".format(captcha_base64))
        # 推送图形验证码
        await self._bs.push_captcha_base64(task_id, captcha_base64)
        # 自动解析图片验证码为文本
        # _t.decode_image(captcha_base64)
        # _text = _t.detect_text(FILENAME)
        # captcha = _text.replace(" ", "").replace("\n", "")
        # logger.info("解析图片验证码之后，获取的文本验证码：{}".format(captcha))
        count = 1
        while count <= 260:
            # await asyncio.sleep(1)
            print('sleep_time', count)
            # await asyncio.sleep(count)
            res = await self._bs.get_login_info(bot_id, task_id)
            logger.debug('获取登录数据：{}'.format(res))
            if res['code'].__eq__(ResponseCode.Refresh_Captcha.value):
                await self._mbd.refresh_captcha(page)
                await asyncio.sleep(.5)
                # _t.decode_image(captcha_base64)
                # _text = _t.detect_text(FILENAME)
                _base64 = await self._mbd.get_captcha_base64(page)
                logger.debug("获取到的验证码为：{}".format(_base64))
                # 推送图形验证码
                await self._bs.push_captcha_base64(task_id, _base64)
                continue
            elif res['code'].__eq__(ResponseCode.Success.value):
                # res['data']['username']
                await self._mbd.login(page, res['data']['userName'], res['data']['password'],
                                      res['data']['captcha'])
                is_check_login, msg = await self._mbd.check_login_err(page)
                logger.debug("is_check_login:{}".format(is_check_login))
                if is_check_login:
                    await self._bd.reload_page(page)
                    result_failed = LoginResult(errMsg=msg)
                    await self._bs.push_login_result(result_failed, task_id)
                    continue
                await asyncio.sleep(.5)
                # 获取余额
                if_true, balance = await self._mbd.check_balance(page)
                if if_true:
                    result_ok = LoginResult(bank_trade_no='0000', balance=balance,
                                            status=ResponseCode.Ok.value)
                    logger.debug("当前余额为：{}".format(balance))
                    # 推送OTP验证结果
                    await self._bs.push_otp_intermediate_result(result_ok, task_id)
                    # 推送登录结果
                    await self._bs.push_login_result(result_ok, task_id)
                # 进入转账页面
                await self._mbd.open_transfer_url(page)
                # 判断姓名是否匹配
                if_check_name, ele_name = await self._mbd.transfer(page, payeeBankCode,
                                                                   payeeBankCard, payee, amount,
                                                                   orderNo)
                if if_check_name.__eq__(False):
                    self.status = ResponseCode.Failed.value
                    self.bank_trade_no = "finish"
                    self.summary = "收款卡姓名校验失败，后台配置姓名：%s,元素定位姓名：%s，支付失败" % (payee, ele_name)
                    # 构造支付结果数据
                    pay_result = PayResult(payer=payeeBankCard, status=self.status,
                                           bank_trade_no=orderNo,
                                           summary=self.summary)
                    # 推送OTP验证结果
                    await self._bs.push_otp_intermediate_result(pay_result, task_id)
                    # 推送支付结果
                    await self._bs.push_pay_result(pay_result, task_id)
                    # 关闭浏览器
                    await self._bd.close(browser)
                    break
                await asyncio.sleep(.5)
                await self._mbd.transfer_base_confirm(page)
                await self._mbd.transfer_send_otp(page)
                otp_base64 = await self._mbd.transfer_get_otp_base64(page)
                logger.debug("获取的OTP二维码为：{}".format(otp_base64.__dict__))
                # 推送OTP
                await self._bs.push_otp_qr_result(otp_base64, task_id)

                # 获取OTP
                otp = await self.mb_try_get_otp(task_id)
                if otp is None:
                    break
                # 输入OTP
                await self._mbd.transfer_input_otp(page, otp)
                # 提交转账交易
                await self._mbd.transfer_submit_otp(page)
                # 判断交易是否成功
                # if_transfer_success = await self._mbd.transfer_success_icon(page)
                is_check_otp, msg = await self._mbd.check_otp_err(page)
                logger.debug("OTP交易结果，是否出现错误提示框：{}，错误信息：{}".format(is_check_otp, msg))
                # if if_transfer_success:
                #     await self.assert_transfer_success()
                #     break
                if is_check_otp:
                    logger.debug("进入OTP错误业务流程")
                    result = await self.assert_transfer_otp(page, task_id)
                    # 推送otp验证结果x
                    await self._bs.push_otp_intermediate_result(result, task_id)
                    # 提交支付结果
                    await self._bs.push_pay_result(result, task_id)
                    await update_task(task_id, 'Done')
                    break
                else:
                    logger.debug("进入OTP正确支付流程")
                    await self.assert_transfer_success(task_id)
                    await update_task(task_id, 'Done')
                    break
            sleep(1)
            count += 1

    async def mb_app(self):
        browser = await self._bd.browser()
        page = await self._bd.pages(browser)
        # 访问网银地址
        await self._mbd.open_login_url(page)
        await self.transfer_app(browser, page, self._bot_id, self._task_id, self._payeeBankCode,
                                self._payeeBankCard, self._payee, self._amount, self._orderNo)
        await browser.close()
