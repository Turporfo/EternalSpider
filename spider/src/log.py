"""Log config"""

import logging
import colorama

def ft(color, reset):
    return f'{color}%(asctime)s  %(filename)s **%(name)s**: [%(levelname)s] %(message)s{reset}'
    
class CustomFormatter(logging.Formatter):
    """重构log"""
    
    # GREEN = "\x1b[38;5;22m"
    # BACK_GREEN = "\x1b[37;42m"
    # YELLOW = "\x1b[33;20m"
    # RED = "\x1b[31;20m"
    # BOLD_RED = "\x1b[31;1m"
    # RESET_ = "\x1b[0m"
    
    GREEN = colorama.Fore.GREEN
    BACK_GREEN = colorama.Back.GREEN
    YELLOW = colorama.Fore.YELLOW
    RED = colorama.Fore.RED
    BOLD_RED = colorama.Fore.RED+colorama.Style.UNDERLINE
    RESET_ = colorama.Style.RESET_ALL
    dateFmt  = '%Y-%m-%d %A %H:%M:%S',
    
    FORMATS = {
        logging.INFO: ft(GREEN, RESET_),
        logging.DEBUG: ft(BACK_GREEN, RESET_),
        logging.WARNING: ft(YELLOW, RESET_),
        logging.ERROR: ft(RED, RESET_),
        logging.CRITICAL: ft(BOLD_RED, RESET_)
    }

    def format(self, record):
        logFormat = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(logFormat)
        return formatter.format(record)

def log_config(log_name, log_level=logging.INFO):
    """Config logging"""
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger


