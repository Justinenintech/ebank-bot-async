# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base_driver.py
# Time       ：2022/5/2 6:32 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import asyncio

import pyppeteer
from loguru import logger

from src.base.tools import Tools


class BaseDriver:
    """
    银行基础驱动类
    """

    def __init__(self):
        self._t = Tools()

    async def pages(self, browser):
        page = await browser.newPage()
        print('page', type(page))
        width, height = self._t.screen_size()
        # 是否启用JS，enabled设为False，则无渲染效果
        await page.setJavaScriptEnabled(enabled=True)
        await page.setViewport({'width': width, 'height': height})
        page.setDefaultNavigationTimeout(60 * 1000)
        return page

    async def browser(self):
        browser = await pyppeteer.launch(
            {'headless': False,
             'devtools': False,
             # 'autoClose': True,
             # 'userDataDir': '/Users/eagle/Ebank/ebank-bot-async/src/cache/mb/userdata',
             # 'executablePath': 'http://127.0.0.1:4444/wd/hub',
             # 'browserWSEndpoint': 'ws://127.0.0.1:4444/devtools/3a133e700db3141d67664b949e6cba7b',
             'args': [
                 # '--disable-extensions',
                 # '--hide-scrollbars',
                 # '--disable-bundled-ppapi-flash',
                 # '--mute-audio',
                 '--disable-infobars',
                 '--no-sandbox',
                 # '--disable-setuid-sandbox',
                 '--disable-gpu',
                 # '--start-maximized',
                 # '--disable-dev-shm-usage',
                 # '--no-first-run',
                 # '--no-zygote',
                 # '--deterministic-fetch',
                 # '--disable-features=IsolateOrigins',
                 # '--disable-site-isolation-trials',
                 '--start-fullscreen',
             ],
             # 'dumpio': True,
             })
        return browser


    async def open_url(self, page, url):
        # print('goto')
        # await asyncio.wait_for(page.goto(url), timeout=120)
        # width, height = self._t.screen_size()
        # await page.setViewport({'width': width, 'height': height})
        # await asyncio.wait_for(page.goto(url, {'waitUntil': 'load'}))
        await page.goto(url, {'waitUntil': 'load'})

    async def reload_page(self, page):
        """
        刷新页面
        :param page:
        :return:
        """
        await page.reload()

    async def close(self, browser):
        """
        关闭浏览器
        :param browser: 浏览器对象
        :return:
        """
        await browser.close()

    async def type_element(self, page, ele: str, parameter):
        """
        输入事件
        :param parameter: str Thuy301097@
        :return:
        """
        await asyncio.gather(
            page.waitForSelector(ele, {'visible': True}),
            page.evaluate(
                'document.querySelector("%s").value=""' % ele),
            page.type(ele, parameter),
        )

    async def get_property(self, page, ele: str, attribute: str):
        """
        根据元素定位-获取任意属性值的内容
        :param page: 浏览器页面元素对象
        :return:
        """

        ele_captcha = await page.J(ele)
        while not await (await ele_captcha.getProperty(attribute)).jsonValue():
            pass
        await page.waitForSelector(ele, {'visible': True})
        base64 = await (await ele_captcha.getProperty(attribute)).jsonValue()
        return base64

    async def hover_element(self, page, ele: str):
        await asyncio.gather(
            page.waitForSelector(ele, {'visible': True}),
            page.hover(ele)
        )

    async def click_element(self, page, ele: str, attribute=None, text=None):
        """
        点击事件
        :param captcha: str Thuy301097@
        :return:
        """
        if ele[0].__eq__('.') or ele[0].__eq__('#'):
            element = await page.J(ele)
            logger.debug('elementelementelement:{}'.format(element))
            await asyncio.gather(
                page.waitForSelector(ele, {'visible': True}),
                page.click(ele)
            )
        if ele[0].__eq__('/'):
            _jx_ele = await page.xpath(ele)
            _jx_ele.click()
            # _jx_ele.click()
            # logger.debug("判断长度有几个：{}".format(len(_jx_ele)))
            # # _text = await (await _jx_ele.getProperty(attribute)).jsonValue()
            # # logger.debug("文本信息为：{}".format(_text))
            # # await page.click(_jx_ele)
            # for _ in _jx_ele:
            #     _text = await (await _.getProperty(attribute)).jsonValue()
            #     logger.debug("文本信息为：{}".format(_text))
            #     if _text.__eq__(text):
            #         await page.click(_)
            # _jx_ele.click()
            # await asyncio.gather(
            #     page.waitForSelector(_jx_ele, {'visible': True}),
            #     _jx_ele.click(),
            # )

    async def check_element_not_equal(self, page, ele: str, expression: str):
        """
        判断元素是否存在，且元素的值不等于None
        :param page:
        :param ele:
        :param expression:
        :return:
        """
        await page.waitForSelector(ele, {'visible': True})
        is_check = await page.Jeval(ele, expression)
        _balance = ''.join(list(filter(str.isdigit, is_check)))
        if _balance != None:
            return True, _balance
        else:
            return False, None

    async def check_element_equal(self, page, ele_btn: str, ele_msg: str, expression: str,
                                  expected: str):
        """
        判断元素是否存在，且元素的值是否等于预期值
        :param page:
        :param ele_btn:
        :param ele_msg:
        :param expression:
        :return:
        """
        # await asyncio.sleep(.5)
        await page.waitForSelector(ele_btn, {'visible': True})
        is_check = await page.Jeval(ele_btn, expression)
        if is_check.replace(" ", "").replace("\n", "").__eq__(expected):
            msg = await page.Jeval(ele_msg, expression)
            return True, msg
        else:
            return False, False

    async def check_otp_err(self, page, ele_btn: str, ele_msg: str, expression: str,
                                  expected: str):
        """
        判断元素是否存在，且元素的值是否等于预期值
        :param page:
        :param ele_btn:
        :param ele_msg:
        :param expression:
        :return:
        """
        # await asyncio.sleep(.5)
        await page.waitForSelector(ele_btn, {'visible': True, 'timeout': 1000 * 1})
        is_check = await page.Jeval(ele_btn, expression)
        if is_check.replace(" ", "").replace("\n", "").__eq__(expected):
            msg = await page.Jeval(ele_msg, expression)
            return True, msg
        else:
            return False, False
