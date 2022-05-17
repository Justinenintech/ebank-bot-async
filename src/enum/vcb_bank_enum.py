# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : vcb_bank_enum.py
# Time       ：2022/4/6 11:19 上午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from enum import Enum, unique


@unique
class VCBElementEnum(Enum):
    """
    VCB-越南外贸银行-银行转账业务-页面元素定位枚举类
    """
    # VCB银行OTP倒计时，两分钟
    VCB_OTP_COUNTDOWN = 110
    # VCB银行登录界面URL
    LOGIN_URL = "https://vcbdigibank.vietcombank.com.vn/login"
    # VIB银行跨行转账界面URL，普通跨行转账
    TRANSFER_INTER = "https://vcbdigibank.vietcombank.com.vn/chuyentien/chuyentienquanhnn"
    # VIB银行同行转账页面URL
    TRANSFER_PEER = "https://vcbdigibank.vietcombank.com.vn/chuyentien/chuyentientronghethong"
    # VCB 跨行-快速汇款转账
    TRANSFER_INSTANT = "https://vcbdigibank.vietcombank.com.vn/chuyentien/chuyentienquataikhoan"
    # VCB 账户详情
    TRANSFER_ACCOUNT_DETAILS = "https://vcbdigibank.vietcombank.com.vn/thongtintaikhoan/chitiettaikhoan"
    # VIB银行编码
    VCB_BANK = "VCB"
    # 登录账号输入框
    USERNAME = "#username"
    # 登录密码输入框
    PASSWORD = "#app_password_login"
    # 登录按钮
    LOGIN = ['id', 'btnLogin']
    # 图形验证码输入框
    CAPTCHA = ['name', 'captcha']
    # 图形验证码图片
    CAPTCHA_IMG = ['css selector', '.input-group-slot-inner > img']
    # 刷新验证码按鈕
    REFRESH_CAPTCHA = ['css selector', '.ubg-secondary > img']
    # 登录失败，提示信息元素定位（非弹出框提示）
    LOGIN_ERROR = ['css selector', '.login-error']
    # 进入支付账号详情页面
    OPEN_ACCOUNT = ['css selector','.item-link-arrow:nth-child(4)']
    SHOW_BALANCE = ['xpath', '//*[@id="maincontent"]/ng-component/div/div[5]/div[2]/div[1]/div[3]/a/div/div[3]/div[2]/div[1]/label']
    # 获取可用余额
    BALANCE = ['css selector', '.list-info-item:nth-child(6) .text-right']

    """>>>>>>>>>>>>>>>>>>>通用元素<<<<<<<<<<<<<<<<<<<<<"""
    # 同行，即时转账，转账OTP页面，提示信息元素定位
    TRANSFER_OTP_ERR_ELE = ['css selector', '.parsley-required']
    OTP_ERR_TEXT_1 = "Quý khách vui lòng nhập OTP"
    OTP_ERR_TEXT_2 = "OTP phải đủ 6 ký tự, Quý khách vui lòng kiểm tra lại"
    OTP_ERR_TEXT_3 = 'OTP错误，尚未获取，明天在处理'
    # 同行、即时转账，转账确认页面，图形验证码图片定位
    TRANSFER_CONFIRM_CAPTCHA_IMG = ['css selector', '.image-captcha > img']

    """>>>>>>>>>>>>>>>>>>>同行转账<<<<<<<<<<<<<<<<<<<<<"""
    # 转账基本信息页面-收款账号
    TRANSFER_PEER_ACCOUNT = ['css selector', '.input-ic-sm-2']
    # 转账基本信息页面-转账金额
    TRANSFER_PEER_AMOUNT = ['css selector', '.col-sm-8 > .live-search-box']
    # 转账基本信息页面-转账备注
    TRANSFER_PEER_REMARK = ['css selector', '.textarea-autosize']
    # 转账基本信息页面-下一步
    TRANSFER_PEER_BASE_NEXT = ['css selector', '.ubtn-big > .ubtn']
    # 转账确认页面-验证码输入框
    TRANSFER_PEER_CONFIRM_CAPTCHA = ['name', 'captchaValue']
    # 转账确认页面-验证码刷新按钮
    TRANSFER_PEER_CONFIRM_REFRESH_CAPTCHA = ['css selector', '.ubg-trans:nth-child(2)']
    # 转账确认页面-下一步，进入OTP输入页面
    TRANSFER_PEER_CONFIRM_NEXT = ['css selector', '.col-6 .ubg-primary > .ubtn-text']
    # 转账OTP页面-OTP输入框
    TRANSFER_PEER_OTP = ['name', 'authValue']
    # 转账OTP页面-下一步
    TRANSFER_PEER_OTP_NEXT = ['css selector','.col-6 .ubg-primary']

    """>>>>>>>>>>>>>>>>>>>即时转账<<<<<<<<<<<<<<<<<<<<<"""
    # 转账基本信息页面-收款账号
    TRANSFER_INSTANT_ACCOUNT = ['id', 'SoTaiKhoanNguoiHuong']
    # 转账基本信息页面-展开银行下拉框列表
    TRANSFER_INSTANT_SELECT_BANK = ['css selector', '.select2-selection__placeholder']
    # 转账基本信息页面-输入要选中的银行编码
    TRANSFER_INSTANT_INPUT_BANK = ['css selector', '.select2-search__field']
    # 转账基本信息页面-选中银行
    TRANSFER_INSTANT_SELECTED_BANK = ['xpath', "//ul[@class='select2-results__options']/li"]
    # 转账基本信息页面-校验选中银行是否正确-元素定位，获取text属性
    TRANSFER_INSTANT_CHECK_SELECTED_BANK = ['id','select2-l922-container']
    # 转账基本信息页面-转账金额
    TRANSFER_INSTANT_AMOUNT = ['id', 'SoTien']
    # 转账基本信息页面-转账备注
    TRANSFER_INSTANT_REMARK = ['css selector', '.col-sm-8 > .ng-untouched']
    # 转账基本信息页面-下一步
    TRANSFER_INSTANT_BASE_NEXT = ['css selector', '.ubtn-wrap-width-md .ubtn-text']
    # 转账确认页面，图形验证码输入框
    TRANSFER_INSTANT_CONFIRM_CAPTCHA = ['css selector', '.ng-dirty:nth-child(1)']
    # 转账确认页面，图形验证码刷新按钮
    TRANSFER_INSTANT_CONFIRM_REFRESH_CAPTCHA = ['css selector', '.ubtn-circle-md > .ng-star-inserted']
    # 转账确认页面，下一步，进入OTP输入页面 转账OTP页面，提交OTP，进入最后一步的页面
    TRANSFER_INSTANT_NEXT = ['css selector', '.ubtn-wrap-width-md > .ubg-primary > .ubtn-text']
    # 转账OTP页面，OTP输入框
    TRANSFER_INSTANT_OTP = ['xpath', "//*[@id='Step3']/div/div/div/div/div/input"]
    # 转账OTP页面，提交OTP，进入最后一步的页面
    # TRANSFER_SUBMIT_OTP = ['css selector', '.ubtn-wrap-width-md > .ubg-primary > .ubtn-text']

    """>>>>>>>>>>>>>>>>>>>>>>>>>>>>>错误提示信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"""
    # 登录失败，验证码错误提示信息
    LOGIN_ERROR_CAPTCHA = "Mã kiểm tra không chính xác"
    # 登录失败，用户名或密码错误 不能用等于 需要使用IN
    LOGIN_ERROR_SERVICE_LOCK = "Tên đăng nhập hoặc mật khẩu không chính xác"
    # 登录失败，用户名或密码错误原始信息
    """
    Tên đăng nhập hoặc mật khẩu không chính xác. Quý khách lưu ý dịch vụ VCB Digibank sẽ bị TẠM KHÓA nếu Quý khách nhập sai mật khẩu liên tiếp 05 LẦN. Quý khách có thể thực hiện cấp lại mật khẩu tại tính năng Quên mật khẩu ở màn hình đăng nhập VCB Digibank trên website Vietcombank hoặc ứng dụng VCB Digibank, tại Quầy giao dịch hoặc liên hệ Hotline 24/7: 1900545413 (dành cho Khách hàng thường) hoặc 18001565 (dành cho Khách hàng ưu tiên) để được hỗ trợ.
    """

    # 弹出框提示信息，登录会话过期
    "Phiên đăng nhập đã hết hiệu lực. Cảm ơn Quý khách đã sử dụng dịch vụ ngân hàng số VCB Digibank"

    # 请输入OTP
    "Quý khách vui lòng nhập mã OTP"
