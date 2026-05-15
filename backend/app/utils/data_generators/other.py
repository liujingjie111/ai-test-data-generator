import random
import string
import uuid
import datetime


DOMAINS = ['example.com', 'test.com', 'sample.org', 'demo.net', 'company.cn', 'site.com']


def generate_uuid() -> str:
    """生成UUID字符串"""
    return str(uuid.uuid4())


def generate_ip() -> str:
    """生成IPv4地址"""
    return f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}'


def generate_mac() -> str:
    """生成MAC地址"""
    return ':'.join(f'{random.randint(0, 255):02x}' for _ in range(6))


def generate_url() -> str:
    """生成随机URL"""
    protocol = random.choice(['http', 'https'])
    domain = random.choice(DOMAINS)
    path_length = random.randint(1, 3)
    paths = []
    for _ in range(path_length):
        path_chars = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 10)))
        paths.append(path_chars)
    path = '/'.join(paths)
    return f'{protocol}://www.{domain}/{path}'


def generate_timestamp() -> str:
    """生成北京时间的ISO格式时间戳"""
    beijing_tz = datetime.timezone(datetime.timedelta(hours=8))
    dt = datetime.datetime.now(beijing_tz)
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def generate_random_string(length: int = 10) -> str:
    """生成指定长度的随机字符串(字母+数字)"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
