import random


PROVINCES = [
    '北京市', '天津市', '上海市', '重庆市',
    '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省',
    '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省',
    '河南省', '湖北省', '湖南省', '广东省', '海南省',
    '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省',
    '台湾省', '内蒙古自治区', '广西壮族自治区', '西藏自治区', '宁夏回族自治区', '新疆维吾尔自治区',
]

CITIES = {
    '北京市': ['东城区', '西城区', '朝阳区', '海淀区', '丰台区', '石景山区', '通州区'],
    '天津市': ['和平区', '河东区', '河西区', '南开区', '河北区', '红桥区', '滨海新区'],
    '上海市': ['黄浦区', '徐汇区', '长宁区', '静安区', '普陀区', '虹口区', '浦东新区'],
    '重庆市': ['渝中区', '大渡口区', '江北区', '沙坪坝区', '九龙坡区', '南岸区'],
    '河北省': ['石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市'],
    '山西省': ['太原市', '大同市', '阳泉市', '长治市', '晋城市', '朔州市'],
    '辽宁省': ['沈阳市', '大连市', '鞍山市', '抚顺市', '本溪市', '丹东市'],
    '吉林省': ['长春市', '吉林市', '四平市', '辽源市', '通化市', '白山市'],
    '黑龙江省': ['哈尔滨市', '齐齐哈尔市', '鸡西市', '鹤岗市', '双鸭山市', '大庆市'],
    '江苏省': ['南京市', '无锡市', '徐州市', '常州市', '苏州市', '南通市'],
    '浙江省': ['杭州市', '宁波市', '温州市', '嘉兴市', '湖州市', '绍兴市'],
    '安徽省': ['合肥市', '芜湖市', '蚌埠市', '淮南市', '马鞍山市', '淮北市'],
    '福建省': ['福州市', '厦门市', '莆田市', '三明市', '泉州市', '漳州市'],
    '江西省': ['南昌市', '景德镇市', '萍乡市', '九江市', '新余市', '鹰潭市'],
    '山东省': ['济南市', '青岛市', '淄博市', '枣庄市', '东营市', '烟台市'],
    '河南省': ['郑州市', '开封市', '洛阳市', '平顶山市', '安阳市', '鹤壁市'],
    '湖北省': ['武汉市', '黄石市', '十堰市', '宜昌市', '襄阳市', '鄂州市'],
    '湖南省': ['长沙市', '株洲市', '湘潭市', '衡阳市', '邵阳市', '岳阳市'],
    '广东省': ['广州市', '深圳市', '珠海市', '汕头市', '佛山市', '韶关市'],
    '海南省': ['海口市', '三亚市', '三沙市', '儋州市'],
    '四川省': ['成都市', '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市'],
    '贵州省': ['贵阳市', '六盘水市', '遵义市', '安顺市', '毕节市', '铜仁市'],
    '云南省': ['昆明市', '曲靖市', '玉溪市', '保山市', '昭通市', '丽江市'],
    '陕西省': ['西安市', '铜川市', '宝鸡市', '咸阳市', '渭南市', '延安市'],
    '甘肃省': ['兰州市', '嘉峪关市', '金昌市', '白银市', '天水市', '武威市'],
    '青海省': ['西宁市', '海东市'],
    '台湾省': ['台北市', '高雄市', '台中市', '台南市'],
    '内蒙古自治区': ['呼和浩特市', '包头市', '乌海市', '赤峰市', '通辽市'],
    '广西壮族自治区': ['南宁市', '柳州市', '桂林市', '梧州市', '北海市'],
    '西藏自治区': ['拉萨市', '日喀则市', '昌都市', '林芝市'],
    '宁夏回族自治区': ['银川市', '石嘴山市', '吴忠市', '固原市'],
    '新疆维吾尔自治区': ['乌鲁木齐市', '克拉玛依市', '吐鲁番市', '哈密市'],
}

STREETS = [
    '中山路', '人民路', '建设路', '解放路', '和平路', '光明路', '文化路',
    '胜利路', '团结路', '幸福路', '复兴路', '民主路', '科学路', '教育路',
    '健康路', '平安路', '振兴路', '创业路', '发展路', '迎宾路',
]

STREET_SUFFIXES = ['街', '道', '巷', '弄']

BUILDING_TYPES = ['小区', '大厦', '花园', '公寓', '广场', '中心', '苑', '庭']


def generate_province() -> str:
    """随机生成中国省份名称"""
    return random.choice(PROVINCES)


def generate_city(province: str = None) -> str:
    """根据省份生成城市名称,如未指定省份则随机选择"""
    if province is None:
        province = random.choice(list(CITIES.keys()))
    if province in CITIES and CITIES[province]:
        return random.choice(CITIES[province])
    return '市区'


def generate_district(city: str = None) -> str:
    """生成区县名称,如未指定城市则随机选择"""
    if city is None:
        all_districts = []
        for districts in CITIES.values():
            all_districts.extend(districts)
        return random.choice(all_districts) if all_districts else '某区'
    for province, cities in CITIES.items():
        if city in cities:
            return city
    return city


def generate_address() -> str:
    """生成详细地址(街道+门牌号+建筑)"""
    street = random.choice(STREETS)
    suffix = random.choice(STREET_SUFFIXES)
    number = random.randint(1, 999)
    building_type = random.choice(BUILDING_TYPES)
    building_name = f'{random.choice(["金", "华", "宏", "利", "万", "瑞", "恒", "信"])}{building_type}'
    room = f'{random.randint(1, 30)}栋{random.randint(101, 2803)}室'
    return f'{street}{suffix}{number}号{building_name}{room}'


def generate_postcode() -> str:
    """生成6位邮政编码"""
    return f'{random.randint(100000, 999999)}'


def generate_latitude() -> float:
    """生成纬度(-90到90)"""
    return round(random.uniform(-90.0, 90.0), 6)


def generate_longitude() -> float:
    """生成经度(-180到180)"""
    return round(random.uniform(-180.0, 180.0), 6)


def generate_full_address() -> str:
    """生成完整地址(省+市+区+详细地址)"""
    province = generate_province()
    city = generate_city(province)
    district = generate_district(city)
    detail = generate_address()
    return f'{province}{city}{district}{detail}'
