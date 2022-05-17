# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : resp_code_enum.py
# Time       ：2022/4/11 11:33 上午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from enum import Enum, unique


@unique
class ResponseCode(Enum):
    """
    响应类型编码
    """
    Success = "0000"

    NotExistTask = '9006'

    """
    刷新验证码
    """
    Refresh_Captcha = "8000"

    """
    成功
    """
    Ok = "Success"

    """
    失败
    """
    Failed = "Failure"

    """
    OTP输入错误，最多允许重试1次
    """
    OTP_ERROR = "Otp_error"

    """
    OTP最终错误
    """
    FAILED_OTP = "Failure_otp"

    Yes = "Y"
    No = "N"
