import random
import string


COMPANY_SUFFIXES = [
    '科技有限公司', '信息技术有限公司', '网络技术有限公司',
    '电子商务有限公司', '软件有限公司', '智能科技有限公司',
    '数据服务有限公司', '通讯技术有限公司', '自动化有限公司',
    '文化传媒有限公司', '广告有限公司', '咨询有限公司',
    '贸易有限公司', '实业有限公司', '集团有限公司',
    '金融服务有限公司', '投资管理有限公司', '资产管理有限公司',
]

INDUSTRIES = [
    '互联网', '软件服务', '电子商务', '金融科技', '人工智能',
    '大数据', '云计算', '物联网', '区块链', '智能制造',
    '新能源', '生物医药', '医疗器械', '教育培训', '文化传媒',
    '广告传媒', '咨询服务', '物流运输', '餐饮连锁', '零售商贸',
    '房地产', '建筑工程', '环保科技', '农业科技', '新材料',
]

COMPANY_PREFIXES = [
    '华', '中', '国', '腾', '阿', '百', '京', '网', '字', '快',
    '小', '美', '大', '天', '云', '智', '创', '新', '科', '联',
    '思', '远', '博', '瑞', '恒', '信', '万', '通', '达', '盛',
]


def generate_company_name() -> str:
    """生成中文公司名称"""
    prefix_length = random.randint(2, 4)
    prefix = ''.join(random.choice(COMPANY_PREFIXES) for _ in range(prefix_length))
    suffix = random.choice(COMPANY_SUFFIXES)
    return prefix + suffix


def generate_credit_code() -> str:
    """生成18位统一社会信用代码"""
    code_chars = '0123456789ABCDEFGHJKLMNPQRTUWXY'

    department_code = f'{random.randint(11, 99):02d}'
    organization_type = f'{random.randint(10, 99):02d}'
    region_code = f'{random.randint(100000, 999999)}'
    org_code = ''.join(random.choice(code_chars) for _ in range(9))

    base_code = department_code + organization_type + region_code + org_code

    weights = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
    total = sum(code_chars.index(base_code[i]) * weights[i] for i in range(17))
    check_code = code_chars[(31 - (total % 31)) % 31]

    return base_code + check_code


def generate_industry() -> str:
    """随机生成行业类型"""
    return random.choice(INDUSTRIES)


def generate_company_phone() -> str:
    """生成企业电话号码"""
    area_codes = ['010', '021', '020', '0755', '0571', '025', '028', '027', '0512', '0532']
    area_code = random.choice(area_codes)
    number = f'{random.randint(10000000, 99999999)}'
    return f'{area_code}-{number}'


def generate_company_address() -> str:
    """生成企业注册地址"""
    province = random.choice([
        '北京市', '上海市', '广州市', '深圳市', '杭州市',
        '南京市', '成都市', '武汉市', '重庆市', '天津市',
    ])
    district = random.choice([
        '朝阳区', '海淀区', '浦东新区', '天河区', '南山区',
        '西湖区', '武侯区', '江岸区', '渝北区', '和平区',
    ])
    street = random.choice([
        '科技园', '软件园', '创新中心', '金融街', '商务大厦',
        '创业园', '产业园', '孵化器', '写字楼', '广场',
    ])
    room = f'{random.randint(1, 50)}层{random.randint(100, 2800)}室'
    return f'{province}{district}{street}{room}'
