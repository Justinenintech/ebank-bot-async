# coding=utf-8
import os

# 系统服务地址
SERVER_HOST = "http://zt.cg45.xyz:31180"

# 任务获取频率 单位秒
FREQUENCY_TIME = 5

# 心跳上报频率 30s
HEARTBEAT_TIME = 30

# 机器人序列号
SERIAL = 'LHS7N18A15003613'

SERVICE_TYPE = 'Payment'
# 公司编码
CODE = "0txff"

_basedir = os.path.abspath(os.path.dirname(__file__))
SERVICE_ACCOUNT = os.path.join(_basedir, 'service-account.json')
FILENAME = os.path.join(_basedir+'/src/img', 'captcha.png')
# 用于MB银行校验是否成功支付
MB_ASSERT_PAY_ONE = os.path.join(_basedir, 'src/img/mb',
                                 'success.png')
MB_ASSERT_PAY_TWO = os.path.join(_basedir, 'src/img/mb',
                                 'down_success.png')
del os
