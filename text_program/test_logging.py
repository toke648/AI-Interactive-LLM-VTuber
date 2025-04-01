import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 替换 print
logging.info("This is an info message")
logging.debug("This is a debug message")  # 仅在 DEBUG 级别下输出
logging.warning("This is a warning message")
logging.error("This is an error message")