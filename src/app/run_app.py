# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : run_app.py
# Time       ：2022/4/13 11:48 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from src.app.mb_app import MBApp, Tracer


class RunApp:
    def __init__(self):
        pass

    async def app_model(self, semaphore, bot_id: str, task_id: str, bankCode: str,
                        payeeBankCode: str,
                        payeeBankCard: str, payee: str, amount: str, orderNo: str):

        async with semaphore:
            if bankCode.lower().__eq__('VCB'.lower()):
                pass
            elif bankCode.lower().__eq__('MBBANK'.lower()):
                _mb = MBApp(bot_id, task_id, payeeBankCode,
                            payeeBankCard, payee, amount, orderNo)
                # Tracer(task_id)
                await _mb.mb_app()
