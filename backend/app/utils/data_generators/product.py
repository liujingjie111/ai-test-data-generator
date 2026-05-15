import random


PRODUCT_ADJECTIVES = [
    '智能', '高清', '无线', '便携式', '时尚', '经典', '豪华', '专业',
    '超薄', '迷你', '多功能', '高效', '环保', '节能', '自动',
]

PRODUCT_NOUNS = [
    '手机', '平板电脑', '笔记本电脑', '耳机', '音箱', '摄像头', '手表',
    '键盘', '鼠标', '显示器', '投影仪', '路由器', '充电宝', '手环',
    '空气净化器', '加湿器', '电风扇', '电水壶', '电饭煲', '吸尘器',
    '运动鞋', '背包', '眼镜', '围巾', '帽子', 'T恤', '衬衫', '夹克',
]

PRODUCT_CATEGORIES = [
    '电子产品', '服装鞋帽', '食品饮料', '家居用品', '美妆护肤',
    '运动户外', '图书音像', '母婴用品', '汽车用品', '办公用品',
    '医疗器械', '五金工具', '宠物用品', '玩具乐器', '珠宝饰品',
]

PRODUCT_BRANDS = [
    '华为', '小米', '苹果', '三星', '联想', '戴尔', '惠普', '华硕',
    'OPPO', 'vivo', '海尔', '美的', '格力', '索尼', '松下', '飞利浦',
]


def generate_product_name() -> str:
    """生成中文产品名称"""
    brand = random.choice(PRODUCT_BRANDS)
    adjective = random.choice(PRODUCT_ADJECTIVES)
    noun = random.choice(PRODUCT_NOUNS)
    model = f'{random.choice("ABCDE")}{random.randint(100, 9999)}'
    return f'{brand}{adjective}{noun}{model}'


def generate_sku() -> str:
    """生成SKU编码(格式: SKU-XXXXXXXXXX)"""
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    code = ''.join(random.choice(chars) for _ in range(10))
    return f'SKU-{code}'


def generate_price(min_price: float = 1, max_price: float = 10000) -> float:
    """生成商品价格"""
    price = random.uniform(min_price, max_price)
    return round(price, 2)


def generate_stock(min_stock: int = 0, max_stock: int = 10000) -> int:
    """生成商品库存数量"""
    return random.randint(min_stock, max_stock)


def generate_category() -> str:
    """随机生成产品类别"""
    return random.choice(PRODUCT_CATEGORIES)
