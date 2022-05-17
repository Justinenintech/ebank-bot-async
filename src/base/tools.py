# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : tools.py
# Time       ：2022/4/8 2:51 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import base64
import os
import re
import socket
import tkinter
import time
import functools
from urllib.request import urlretrieve
from PIL import Image, ImageChops
from setttings import FILENAME, SERVICE_ACCOUNT


class Tools(object):
    def __init__(self):
        pass

    @staticmethod
    def get_ip():
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    @staticmethod
    def screen_size():
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        tk.quit()
        return width, height

    @staticmethod
    def set_timeout(num, callback):
        def run_benchmark(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                res = await func(*args, **kwargs)
                print(f'{func.__name__} run {args}  {round(time.perf_counter() - start_time)}')
                if int(num) >= round(time.perf_counter() - start_time):
                    print('未超时')
                else:
                    await callback()
                return res

            return wrapper

        return run_benchmark

    @staticmethod
    def decode_image(src):
        """
        解码图片
        :param src: 图片编码
            eg:
                src="data:image/gif;base64,R0lGODlhMwAxAIAAAAAAAP///
                    yH5BAAAAAAALAAAAAAzADEAAAK8jI+pBr0PowytzotTtbm/DTqQ6C3hGX
                    ElcraA9jIr66ozVpM3nseUvYP1UEHF0FUUHkNJxhLZfEJNvol06tzwrgd
                    LbXsFZYmSMPnHLB+zNJFbq15+SOf50+6rG7lKOjwV1ibGdhHYRVYVJ9Wn
                    k2HWtLdIWMSH9lfyODZoZTb4xdnpxQSEF9oyOWIqp6gaI9pI1Qo7BijbF
                    ZkoaAtEeiiLeKn72xM7vMZofJy8zJys2UxsCT3kO229LH1tXAAAOw=="

        :return: str 保存到本地的文件名
        """
        # 1、信息提取
        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
        if result:
            ext = result.groupdict().get("ext")
            data = result.groupdict().get("data")

        else:
            raise Exception("Do not parse!")

        # 2、base64解码
        img = base64.urlsafe_b64decode(data)

        # 3、二进制文件保存
        # filename = "{}.{}".format(uuid.uuid4(), ext)
        print('FILENAME', FILENAME)
        filename = FILENAME
        with open(filename, "wb") as f:
            f.write(img)

        return filename

    @staticmethod
    def encode_image(filename):
        """
        编码图片
        :param filename: str 本地图片文件名
        :return: str 编码后的字符串
            eg:
            src="data:image/gif;base64,R0lGODlhMwAxAIAAAAAAAP///
                yH5BAAAAAAALAAAAAAzADEAAAK8jI+pBr0PowytzotTtbm/DTqQ6C3hGX
                ElcraA9jIr66ozVpM3nseUvYP1UEHF0FUUHkNJxhLZfEJNvol06tzwrgd
                LbXsFZYmSMPnHLB+zNJFbq15+SOf50+6rG7lKOjwV1ibGdhHYRVYVJ9Wn
                k2HWtLdIWMSH9lfyODZoZTb4xdnpxQSEF9oyOWIqp6gaI9pI1Qo7BijbF
                ZkoaAtEeiiLeKn72xM7vMZofJy8zJys2UxsCT3kO229LH1tXAAAOw=="

        """
        # 1、文件读取
        ext = filename.split(".")[-1]

        with open(filename, "rb") as f:
            img = f.read()

        # 2、base64编码
        data = base64.b64encode(img).decode()

        # 3、图片编码字符串拼接
        src = "data:image/{ext};base64,{data}".format(ext=ext, data=data)
        return src

    @staticmethod
    def detect_text(path):
        """Detects text in the file."""
        from google.cloud import vision
        import io
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        for text in texts:
            # print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])

            # print('bounds: {}'.format(','.join(vertices)))
            return text.description
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

    @staticmethod
    def compare_images(path_one, path_two, img_url):
        """
        比较图片是否一致
        :return:
        """
        urlretrieve(img_url, path_two)
        img_one = Image.open(path_one)
        img_two = Image.open(path_two)
        try:
            diff = ImageChops.difference(img_one, img_two)
            if diff.getbbox() is None:
                os.remove(path_two)
                return True
            else:
                os.remove(path_two)
                return False
        except ValueError as e:
            os.remove(path_two)
            return "{0}\n{1}".format(e, "图片大小和对应的宽度不一致！")