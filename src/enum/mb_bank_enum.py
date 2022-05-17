# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : mb_bank_enum.py
# Time       ：2022/4/13 2:44 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from enum import Enum, unique


@unique
class MBElementEnum(Enum):
    """
    MB银行转账业务-页面元素定位枚举类
    """
    # MB银行OTP倒计时，两分钟
    MB_OTP_COUNTDOWN = 110
    # MB银行登录界面URL
    BANK_LOGIN_URL = "https://online.mbbank.com.vn/pl/login"
    # MB银行转账界面URL
    BANK_TRANSFER_URL = "https://online.mbbank.com.vn/transfer/inhouse"

    # MB银行编码
    MB_BANK = "MBbank"
    # 登录账号输入框
    USERNAME = "#user-id"
    # 登录密码输入框
    PASSWORD = "#new-password"
    # 验证码输入框
    CAPTCHA = '.pl-upper'
    # 图形验证码
    CAPTCHA_BASE64 = '.ng-star-inserted:nth-child(1)'
    # 刷新验证码按鈕
    CAPTCHA_REFRESH = '#refresh-captcha'
    # 登录按钮
    LOGIN = '#login-btn'
    ERROR_BTN = '.btn-primary'
    ERROR_CODE = '.fc-header'
    ERROR_MSG = '.text-center:nth-child(2)'
    # # 登录按钮
    # LOGIN = ['css selector', '.mat-button-wrapper']
    # # 登录失败，弹出提示框的关闭按钮
    # ERROR_BTN = ['css selector', '.btn-primary']
    # 登录成功-首页余额
    # BALANCE = ['css selector', '.gtt-2 > .balance']
    BALANCE = '.gtt-2 > .balance'
    # 出现错误弹窗，空白处
    ERROR_BTN_BACKDROP = ['css selector', '.cdk-overlay-backdrop']

    # otp错误，弹出框
    OTP_ERROR_BTN = ['xpath',
                     "//button[contains(.,'ĐỒNG Ý')]"]

    OTP_ERROR_TEXT = ['xpath',
                      "//span[contains(.,'Mã xác thực không chính xác. Bạn vui lòng thử lại!')]"]
    # 登录失败，密码错误- Mã lỗi: GW21  .fc-header
    # ERROR_CODE = ['css selector', '.fc-header']
    # 登录成功判断
    LOGIN_SUCCESS = ['css selector', '.welcome-back']
    # 登录成功-首页余额
    # BALANCE = ['css selector', '.gtt-2 > .balance']
    # Transfers主菜单
    TRANSFERS_MNU = ['id', 'MNU_GCME_050000']
    # Transfer money-转账页面
    TRANSFER_MONEY = ['css selector', '#MNU_GCME_050301 > .mat-tree-node > .ng-tns-c182-2']
    # 判断是否成功进入转账页面 'Chuyển tiền tới tài khoản ngân hàng
    TRANSFER_MONEY_TEXT = ['css selector', '.lbl-begin']
    # 用于判断的文本信息 assert
    ASSERT_IN_TRANSFER = 'Chuyển tiền tới tài khoản ngân hàng'

    ASSERT_PAYEE_PAYER = ['class name', 'multiline-select']

    # 下一步
    TRANSFER_MONEY_CONTINUE = '.btn-next .btn'
    TRANSFER_BANK_SELECT = '.ng-tns-c115-9 > .mat-select-value'

    # 搜索要选择的银行
    TRANSFER_BANK_SEARCH = '.mat-select-search-inner > .mat-select-search-input'
    # 选中银行
    TRANSFER_BANK_SELECTED = '.option-images-display'
    # 打开银行选择下拉框
    # TRANSFER_BANK_SELECT = '.ng-tns-c115-39 > .mat-select-value'
    # TRANSFER_BANK_SELECT = '//*[@id="mat-select-3"]/div/div[1]/span'
    # TRANSFER_BANK_SELECT = '//*[@id="mat-select-3"]/div/div[1]'
    # TRANSFER_BANK_SELECT = '//*[@id="mat-select-5"]'
    # # TRANSFER_BANK_SELECT = ['xpath', '//*[@id="mat-select-3"]/div/div[1]/span']
    # # 搜索要选择的银行
    #
    # TRANSFER_BANK_SEARCH = '.mat-select-search-inner > .mat-select-search-input'
    # # 选中银行
    # # TRANSFER_BANK_SELECTED = ['xpath',
    # #                           '/html/body/div[2]/div[2]/div/div/div/mat-option/span/div/span']
    # TRANSFER_BANK_SELECTED = '.option-images-display > span'
    # 收款人账号 （假设输入账号错误，账号无效 Mã lỗi: 201
    # TRANSFER_RECEIVER_ACCOUNT = ['css selector', '.form-group:nth-child(3) .form-control']
    TRANSFER_ACCOUNT = '.form-group:nth-child(3) .form-control'
    # 收款人姓名
    # //*[@id="cdk-step-content-3-1"]/div/div/mbb-transfer-body/form/div[3]/div/input
    # TRANSFER_RECEIVER_NAME = ['css selector', '.form-group > .col-sm-8 > .ng-star-inserted']
    TRANSFER_RECEIVER_NAME = '.form-group > .col-sm-8 > .ng-star-inserted'
    # TRANSFER_RECEIVER_NAME = ['xpath',"//*[@id='cdk-step-content-0-1']/div/div/mbb-transfer-body/form/div[3]/div/input"]
    # 越南盾输入框
    # TRANSFER_AMOUNT = '.col-sm-8 > .ng-dirty'
    TRANSFER_AMOUNT = '.form-group:nth-child(5) .form-control'
    # 备注输入框
    # TRANSFER_SUMMARY = '.form-group:nth-child(6) .form-control'
    TRANSFER_REMARK = '.form-group:nth-child(6) .form-control'
    # TRANSFER_BASE_CONFIRM = '.form-group:nth-child(2) .w-100'
    # TRANSFER_BASE_CONFIRM = '//*[@id="cdk-step-content-0-1"]/div/div/div/div/button'
    TRANSFER_BASE_CONFIRM = '#cdk-step-content-0-1 > div > div > div > div > button'
    # TRANSFER_BASE_CONFIRM = 'w-100.btn.btn-header.btn-icon-right.align-self-center'
    # 下一步，生成OTP
    SEND_VERIFY_CODE_OTP = '#cdk-step-content-0-2 > div > div > button'
    # 获取otp base64
    OTP_BASE64 = '.aclass > img'
    # otp输入框
    OTP_INPUT = '.ng-invalid:nth-child(1)'

    # 输入otp 之后点击确认按钮
    OTP_SUBMIT = '.dialog-action > .btn'

    SUCCESS_ICON = '.success-img > img'
    # 转账成功保存截图的按钮
    # "assets/images/email.png"
    # SUCCESS_ICON_XPATH = ['xpath',
    #                       '/html/body/app-root/div/ng-component/div[1]/div/div/div[1]/div/div/div/mbb-transfer-management/div/mbb-transfer-inhouse/div/div[2]/div/div/mat-vertical-stepper/div[4]/div/div/div/div/mbb-transfer-sucsess/div[1]/div[1]/img']
