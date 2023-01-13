import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def color(string: str, color_name: str = 'white') -> str:

    pref = '\033['
    reset = f'{pref}0m'

    ansi_codes = {
        'red': '31m',
        'green': '32m',
        'yellow': '33m',
        'blue': '34m',
        'magenta': '35m',
        'cyan': '36m',
        'white': '37m',
        'reset': '0m'
    }

    return f'{pref}{ansi_codes[color_name]}{string}{reset}'


def show_exec_time(func):
    from time import perf_counter

    def wrapper(*args, **kwargs):
        start = perf_counter()
        return_value = func(*args, **kwargs)
        end = perf_counter()
        execution_time = round((end - start), 2)
        print(f'[*] "{func.__name__}" execution time: {execution_time} s')
        logger.info(f'[*] "{func.__name__}" execution time: {execution_time} s')
        return return_value

    return wrapper


def render_dump_path(config, extraction_timestamp):
    ts_string = extraction_timestamp.strftime('%Y-%m-%d_%H-%M-%S_%f')
    uri = f"{config['load']['sink']['schema']}_{config['load']['sink']['table']}"
    dump_path = f"{config['dump']}/dump_{uri}_{ts_string}"
    return dump_path
