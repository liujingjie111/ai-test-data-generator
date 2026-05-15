import random


CHINESE_BANKS = [
    '中国工商银行', '中国农业银行', '中国银行', '中国建设银行',
    '交通银行', '招商银行', '中信银行', '中国民生银行',
    '中国光大银行', '华夏银行', '广发银行', '平安银行',
    '兴业银行', '上海浦东发展银行', '北京银行', '上海银行',
]


def _luhn_check(card_number: str) -> bool:
    """Luhn校验算法,验证银行卡号是否有效"""
    digits = [int(d) for d in card_number]
    digits.reverse()
    total = 0
    for i, digit in enumerate(digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def _generate_luhn_number(length: int, prefix: str = '') -> str:
    """生成通过Luhn校验的卡号"""
    if prefix:
        base = prefix
    else:
        base = ''

    remaining = length - len(base) - 1
    for _ in range(remaining):
        base += str(random.randint(0, 9))

    total = 0
    reversed_base = base[::-1]
    for i, digit in enumerate(reversed_base):
        d = int(digit)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d

    check_digit = (10 - (total % 10)) % 10
    return base + str(check_digit)


def generate_bank_card() -> str:
    """生成16-19位银行卡号(通过Luhn校验)"""
    length = random.choice([16, 17, 18, 19])
    bank_prefixes = ['62', '95', '60']
    prefix = random.choice(bank_prefixes)
    return _generate_luhn_number(length, prefix)


def generate_credit_card() -> str:
    """生成16位信用卡号(通过Luhn校验)"""
    cc_prefixes = ['4', '51', '52', '53', '54', '55', '35']
    prefix = random.choice(cc_prefixes)
    return _generate_luhn_number(16, prefix)


def generate_bank_name() -> str:
    """随机生成中国银行名称"""
    return random.choice(CHINESE_BANKS)


def generate_amount(min_amount: float = 0, max_amount: float = 100000, decimals: int = 2) -> float:
    """生成指定范围的金额"""
    amount = random.uniform(min_amount, max_amount)
    return round(amount, decimals)
