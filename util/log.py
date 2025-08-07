# logger_config.py
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
import inspect
from pathlib import Path


def get_logger():
    # 获取调用者的文件名（不包含路径和扩展名）
    frame = inspect.currentframe().f_back.f_back  # 跳过两层调用栈
    module = inspect.getmodule(frame)
    if module and module.__file__:
        file_path = Path(module.__file__)
        logger_name = file_path.stem  # 文件名（不含扩展名）
    else:
        logger_name = __name__  # 默认使用当前模块名

    # 创建或获取同名logger
    logger = logging.getLogger(logger_name)

    # 避免重复配置
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # 创建文件处理器
        file_handler = logging.FileHandler("app.log")
        file_handler.setLevel(logging.DEBUG)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
