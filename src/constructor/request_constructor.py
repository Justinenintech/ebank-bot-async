# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : request_constructor.py
# Time       ：2022/5/2 2:31 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from src.enum.resp_code_enum import ResponseCode


class LoginResult:
    """
    登录结果信息
    """

    def __init__(self, payee_card=None,
                 status=ResponseCode.Failed.value,
                 bank_trade_no=None,
                 balance=None,
                 base64ImageCaptcha=None,
                 showSecLoginCode=None,
                 errMsg=None):
        self.payeeCard = payee_card
        self.status = status
        self.bankTradeNo = bank_trade_no
        self.balance = balance
        self.errMsg = errMsg
        self.base64ImageCaptcha = base64ImageCaptcha
        self.showSecLoginCode = ResponseCode.Yes.value if showSecLoginCode else ResponseCode.No.value
        self.isBase64Image = ResponseCode.Yes.value if base64ImageCaptcha else ResponseCode.No.value
        # print('self.showSecLoginCode', self.showSecLoginCode)


class PayResult:
    """
    支付结果类
    """

    def __init__(self, payer=None, status=ResponseCode.Failed.value, bank_trade_no=None, summary=None):
        self.payer = payer
        self.status = status
        self.bankTradeNo = bank_trade_no
        self.summary = summary