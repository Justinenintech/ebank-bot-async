# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : mb_driver.py
# Time       ：2022/5/2 6:39 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import asyncio

import pyppeteer.errors
from loguru import logger

from setttings import MB_ASSERT_PAY_ONE, MB_ASSERT_PAY_TWO
from src.base.tools import Tools
from src.constructor.request_constructor import LoginResult
from src.driver.base_driver import BaseDriver
from src.enum.mb_bank_enum import MBElementEnum
from src.enum.resp_code_enum import ResponseCode


class MBDriver:
    """
    mbBank驱动器
    """

    def __init__(self):
        self._bd = BaseDriver()
        self._ele_username = MBElementEnum.USERNAME.value  # 用户名输入框
        self._ele_password = MBElementEnum.PASSWORD.value  # 密码输入框
        self._ele_captcha = MBElementEnum.CAPTCHA.value  # 验证码输入框
        self._ele_base64 = MBElementEnum.CAPTCHA_BASE64.value  # 获取图形验证码
        self._ele_refresh = MBElementEnum.CAPTCHA_REFRESH.value  # 刷新图形验证码
        self._ele_login = MBElementEnum.LOGIN.value  # 登录按钮
        self._ele_btn = MBElementEnum.ERROR_BTN.value  # 登录弹出框的确认按钮
        self._ele_msg = MBElementEnum.ERROR_MSG.value  # 登录弹出框的msg消息
        self._ele_balance = MBElementEnum.BALANCE.value  # 余额
        self._login_url = MBElementEnum.BANK_LOGIN_URL.value  # 网银地址
        self._transfer_url = MBElementEnum.BANK_TRANSFER_URL.value  # 转账页面URL
        self._transfer_continue = MBElementEnum.TRANSFER_MONEY_CONTINUE.value  # 转账基本信息页面
        self._transfer_select_bank = MBElementEnum.TRANSFER_BANK_SELECT.value  # 展开银行下拉框
        self._transfer_input_bank = MBElementEnum.TRANSFER_BANK_SEARCH.value  # 输入银行编码
        self._transfer_selected_bank = MBElementEnum.TRANSFER_BANK_SELECTED.value  # 选中银行
        self._transfer_account = MBElementEnum.TRANSFER_ACCOUNT.value  # 输入银行收款账号
        self._transfer_name = MBElementEnum.TRANSFER_RECEIVER_NAME.value  # 获取银行账号的姓名
        self._transfer_amount = MBElementEnum.TRANSFER_AMOUNT.value  # 输入转账金额
        self._transfer_remark = MBElementEnum.TRANSFER_REMARK.value  # 输入银行备注
        self._transfer_base_confirm = MBElementEnum.TRANSFER_BASE_CONFIRM.value  # 下一步按钮，进入转账信息确认页面
        self._transfer_send_otp = MBElementEnum.SEND_VERIFY_CODE_OTP.value  # 核对转账信息之后，下一步按钮，产生OTP二维码
        self._transfer_otp_base64 = MBElementEnum.OTP_BASE64.value  # 获取二维码base64
        self._transfer_otp_input = MBElementEnum.OTP_INPUT.value  # OTP输入框
        self._transfer_otp_submit = MBElementEnum.OTP_SUBMIT.value  # 提交OTP，完成转账交易
        self._transfer_success_icon = MBElementEnum.SUCCESS_ICON.value  # 交易成功的图片
        self._get_text = 'node => node.textContent'
        self._get_value = 'value'
        self._expected_value = 'Đóng'
        self._expected_otp_value = 'ĐỒNG Ý'
        self._src = 'src'
        self._t = Tools()

    async def open_login_url(self, page):
        """
        访问网银地址
        :param page:
        :return:
        """
        await self._bd.open_url(page, self._login_url)

    async def open_transfer_url(self, page):
        """
        访问转账页面
        :param page:
        :return:
        """
        await self._bd.open_url(page, self._transfer_url)

    async def get_captcha_base64(self, page):
        """
        获取src属性中的base64
        :param page:
        :return:
        """
        base64 = await self._bd.get_property(page, self._ele_base64, self._src)
        return base64

    async def refresh_captcha(self, page):
        """
        刷新图形验证码
        :param page:
        :return:
        """
        await self._bd.click_element(page, self._ele_refresh)

    async def check_login_err(self, page):
        """
        检测是否出现错误提示框
        :param page:
        :return:
        """
        if_true, is_msg = await self._bd.check_element_equal(page, self._ele_btn, self._ele_msg,
                                                             self._get_text, self._expected_value)
        return if_true, is_msg

    async def check_otp_err(self, page):
        """
        检测是否出现错误提示框
        :param page:
        :return:
        """
        try:
            if_true, is_msg = await self._bd.check_otp_err(page, self._ele_btn, self._ele_msg,
                                                           self._get_text,
                                                           self._expected_otp_value)
            return if_true, is_msg
        except pyppeteer.errors.TimeoutError:
            return False, None

    async def close_top_err(self, page):
        """
        关闭错误提示框
        :param page:
        :return:
        """
        await self._bd.click_element(page, self._ele_btn)

    async def check_balance(self, page):
        """
        获取余额
        :param page:
        :return:
        """
        if_true, balance = await self._bd.check_element_not_equal(page, self._ele_balance,
                                                                  self._get_text)
        return if_true, balance

    async def transfer_base_continue(self, page):
        """
        进入转账基本信息录入步骤
        :param page:
        :return:
        """
        await self._bd.click_element(page, self._transfer_continue)

    async def transfer_selected_bank(self, page, bank):
        """
        选择要转账的银行
        :return:
        """
        await self._bd.click_element(page, self._transfer_select_bank)
        await asyncio.sleep(.3)
        await self._bd.type_element(page, self._transfer_input_bank, bank)
        await asyncio.sleep(.3)
        await self._bd.click_element(page, self._transfer_selected_bank)

    async def transfer_account(self, page, account: str):
        """
        输入收款账号
        :param page:
        :param account: 收款账号
        :return:
        """
        await self._bd.type_element(page, self._transfer_account, account)

    async def transfer_name(self, page, payee):
        """
        校验订单的姓名和元素加载出来的是否一致
        :param page:
        :param payee:订单的银行姓名
        :return:
        """
        name = await self._bd.get_property(page, self._transfer_name, self._get_value)
        logger.debug("姓名是：{}:{}".format(name, payee))
        if name.__eq__(payee):
            return True, name
        else:
            return False, name

    async def transfer_amount(self, page, amount):
        """
        输入转账金额
        :param page:
        :param amount: 金额
        :return:
        """
        await self._bd.type_element(page, self._transfer_amount, amount)

    async def transfer_remark(self, page, remark):
        """
        输入备注信息
        :param page:
        :param remark: 备注内容
        :return:
        """
        await self._bd.type_element(page, self._transfer_remark, remark)

    async def transfer_base_confirm(self, page):
        """
        完成转账基本信息的录入，进入到核对页面
        :param page:
        :return:
        """
        await self._bd.hover_element(page, self._transfer_base_confirm)
        await asyncio.sleep(.5)
        await self._bd.click_element(page, self._transfer_base_confirm)
        # await page.mouse.down()

    async def transfer_send_otp(self, page):
        """
        完成转账信息的核对，进入到生成otp页面
        :param page:
        :return:
        """
        await self._bd.hover_element(page, self._transfer_send_otp)
        await asyncio.sleep(.5)
        await self._bd.click_element(page, self._transfer_send_otp)

    async def transfer_get_otp_base64(self, page):
        """
        根据otp二维码获取其src属性的base64字符串
        :param page:
        :return:
        """
        await asyncio.sleep(.5)
        base64 = await self._bd.get_property(page, self._transfer_otp_base64, self._src)
        logger.debug("OTP二维码:{}".format(base64))
        base64_img = LoginResult(bank_trade_no='0000',
                                 status=ResponseCode.Ok.value,
                                 base64ImageCaptcha=base64)
        return base64_img

    async def transfer_input_otp(self, page, otp):
        """
        输入OTP
        :param page:
        :param otp: 接收到的otp
        :return:
        """
        await self._bd.type_element(page, self._transfer_otp_input, otp)

    async def transfer_submit_otp(self, page):
        """
        提交OTP，完成转账交易
        :param page: class
        :return:
        """
        await self._bd.click_element(page, self._transfer_otp_submit)

    async def transfer_success_icon(self, page):
        """
        判断交易是否成功
        :param page:
        :return:
        """
        await asyncio.sleep(.5)
        img_url = await self._bd.get_property(page, self._transfer_success_icon, self._src)
        is_img = self._t.compare_images(MB_ASSERT_PAY_ONE, MB_ASSERT_PAY_TWO, img_url)
        return is_img

    async def login(self, page, username, password, captcha):
        """
        登录网银
        :param page:
        :param username: 登录账号
        :param password: 登录密码
        :param captcha: 验证码
        :return:
        """
        await self._bd.type_element(page, self._ele_username, username)
        await self._bd.type_element(page, self._ele_password, password)
        await self._bd.type_element(page, self._ele_captcha, captcha)
        await self._bd.click_element(page, self._ele_login)

    async def transfer(self, page, bank: str, payee_account: str, payee: str, amount: str,
                       remark: str):
        """
        转账业务
        :param page:
        :param bank: 收款银行编码
        :param payee_account: 收款银行账号
        :param payee: 账号姓名
        :param amount: 转账金额
        :param remark: 转账备注
        :return:
        """
        await self.transfer_base_continue(page)
        await asyncio.sleep(.5)
        await self.transfer_selected_bank(page, bank)
        await self.transfer_account(page, payee_account)
        await self.transfer_amount(page, amount)
        await self.transfer_remark(page, remark)
        if_true = await self.transfer_name(page, payee)
        logger.debug("姓名是否匹配：{}".format(if_true))
        return if_true
