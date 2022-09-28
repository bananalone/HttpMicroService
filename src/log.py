import time
from pathlib import Path
import logging


# log
def set_logging(
    name: str = None,
    format: str = None,
    stream: bool = True,
    stream_level: int = logging.DEBUG,
    save_path: str | Path = None,
    file_level: int = logging.INFO
    ):
    assert stream or file, 'Select at least one output mode'
    logger = logging.getLogger(name)
    logger.setLevel(logging.NOTSET) # 取消logger等级，按照handle等级记录日志
    formatter = logging.Formatter(format)
    # stream handler
    if stream:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        streamHandler.setLevel(stream_level)
        logger.addHandler(streamHandler)
    # file handler
    if save_path:
        root = Path(save_path)
        if not root.exists():
            root.mkdir()
        file = root / (time.asctime() + '.log')
        fileHandler = logging.FileHandler(file.as_posix(), encoding='utf-8')
        fileHandler.setLevel(file_level)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

