import random
import datetime


CHINESE_SURNAMES = [
    '王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
    '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
    '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧',
    '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕',
    '苏', '卢', '蒋', '蔡', '贾', '丁', '魏', '薛', '叶', '阎',
]

CHINESE_GIVEN_NAMES_MALE = [
    '伟', '强', '磊', '军', '勇', '杰', '涛', '明', '超', '刚',
    '平', '辉', '鹏', '浩', '亮', '龙', '飞', '建', '国庆', '志',
    '文', '建华', '国强', '志强', '文博', '宇航', '天佑', '子轩', '浩然', '雨泽',
]

CHINESE_GIVEN_NAMES_FEMALE = [
    '芳', '娜', '敏', '静', '丽', '艳', '娟', '霞', '玲', '婷',
    '雪', '云', '萍', '蓉', '燕', '蕾', '欣', '颖', '茜', '薇',
    '梦', '雨', '诗', '佳', '思', '美', '慧', '嘉', '悦', '彤',
]

EMAIL_DOMAINS = ['qq.com', '163.com', 'gmail.com', 'sina.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'sohu.com']


def generate_name() -> str:
    """生成中文姓名"""
    surname = random.choice(CHINESE_SURNAMES)
    gender = random.choice(['male', 'female'])
    given_name = random.choice(
        CHINESE_GIVEN_NAMES_MALE if gender == 'male' else CHINESE_GIVEN_NAMES_FEMALE
    )
    return surname + given_name


def generate_id_card() -> str:
    """生成符合校验规则的中国身份证号码(18位)"""
    province_codes = [
        '11', '12', '13', '14', '15', '21', '22', '23',
        '31', '32', '33', '34', '35', '36', '37',
        '41', '42', '43', '44', '45', '46',
        '50', '51', '52', '53', '54',
        '61', '62', '63', '64', '65',
    ]

    province = random.choice(province_codes)
    city = f'{random.randint(0, 99):02d}'
    district = f'{random.randint(0, 99):02d}'

    birth_year = random.randint(1950, 2005)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    birth_date = f'{birth_year:04d}{birth_month:02d}{birth_day:02d}'

    sequence = f'{random.randint(0, 999):03d}'

    base_id = province + city + district + birth_date + sequence

    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    sum_value = sum(int(base_id[i]) * weights[i] for i in range(17))
    check_code = check_codes[sum_value % 11]

    return base_id + check_code


def generate_phone() -> str:
    """生成中国11位手机号"""
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',
                '170', '171', '172', '173', '174', '175', '176', '177', '178']
    prefix = random.choice(prefixes)
    suffix = f'{random.randint(0, 99999999):08d}'
    return prefix + suffix


def generate_email() -> str:
    """生成随机邮箱地址"""
    name_length = random.randint(5, 12)
    name_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    name = ''.join(random.choice(name_chars) for _ in range(name_length))
    domain = random.choice(EMAIL_DOMAINS)
    return f'{name}@{domain}'


def generate_gender() -> str:
    """随机生成性别(男/女)"""
    return random.choice(['男', '女'])


def generate_age(min_age: int = 18, max_age: int = 65) -> int:
    """生成指定范围内的年龄"""
    return random.randint(min_age, max_age)


def generate_birth_date() -> str:
    """生成YYYY-MM-DD格式的出生日期"""
    year = random.randint(1950, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f'{year:04d}-{month:02d}-{day:02d}'
