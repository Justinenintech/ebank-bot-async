# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : run_app.py
# Time       ：2022/4/22 12:59 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""

import json
from concurrent.futures import ThreadPoolExecutor
import asyncio

from loguru import logger

from src.app.mb_app import Tracer
from src.app.run_app import RunApp
from src.enum.run_enum import RunEnum
from src.service.bot_task_service import BaseService
from src.sql_app.crud import get_where_all, update_task

bs = BaseService()
_run = RunApp()
_t = Tracer()


async def run(bot_id):
    """
    程序入口，没有数据时，请求余额接口保持会话，有数据时去校验银行卡（每1秒运行一次）
    :return:
    """
    await bs.pull_task(bot_id)
    tasks = []
    res = await get_where_all(RunEnum.RUN_READY.value)
    datas = [json.loads(_.json()) for _ in res]
    logger.debug("处理后的当前待检测待数据：{}".format(datas))
    logger.debug('datas:{}'.format(datas))
    semaphore = asyncio.Semaphore(len(datas))
    if len(datas).__eq__(0):
        logger.info("当前待转账的任务数量：{}".format(len(datas)))
    else:
        logger.info("当前待转账的任务数量：{}".format(len(datas)))
        for _ in datas:
            await update_task(_['id'], 'Running')
            task = asyncio.create_task(
                _run.app_model(semaphore, bot_id, _['id'], _['bankCode'], _['payeeBankCode'],
                                  _['payeeBankCard'], _['payee'], _['amount'], _['orderNo']))

            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results


def asyncio_schedule(bot_id):
    """
    python version >= 3.4.0
    :return:
    """
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.executors.pool import ProcessPoolExecutor

    try:
        import asyncio
    except ImportError:
        import trollius as asyncio

    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 100
    }
    scheduler = AsyncIOScheduler(job_defaults=job_defaults, executorsexecutors=executors,
                                 timezone='Asia/Shanghai')
    scheduler.add_job(run, 'interval', executor='default', seconds=1, args=[bot_id])
    # scheduler.add_job(t.del_done_task, 'cron', day_of_week='*', hour='1', minute='30', second='30')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot_id = loop.run_until_complete(bs.register())
    if bot_id is None:
        bot_id = loop.run_until_complete(bs.register())
        logger.debug("当前机器人ID：{}".format(bot_id))
        asyncio_schedule(bot_id)
        loop.run_forever()
    else:
        asyncio_schedule(bot_id)
        loop.run_forever()
