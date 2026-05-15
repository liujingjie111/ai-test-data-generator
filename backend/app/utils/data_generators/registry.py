from app.utils.data_generators.personal import (
    generate_name,
    generate_id_card,
    generate_phone,
    generate_email,
    generate_gender,
    generate_age,
    generate_birth_date,
)
from app.utils.data_generators.address import (
    generate_province,
    generate_city,
    generate_district,
    generate_address,
    generate_postcode,
    generate_latitude,
    generate_longitude,
    generate_full_address,
)
from app.utils.data_generators.finance import (
    generate_bank_card,
    generate_credit_card,
    generate_bank_name,
    generate_amount,
)
from app.utils.data_generators.enterprise import (
    generate_company_name,
    generate_credit_code,
    generate_industry,
    generate_company_phone,
    generate_company_address,
)
from app.utils.data_generators.product import (
    generate_product_name,
    generate_sku,
    generate_price,
    generate_stock,
    generate_category,
)
from app.utils.data_generators.other import (
    generate_uuid,
    generate_ip,
    generate_mac,
    generate_url,
    generate_timestamp,
    generate_random_string,
)


GENERATOR_REGISTRY = {
    'name': generate_name,
    'id_card': generate_id_card,
    'phone': generate_phone,
    'email': generate_email,
    'gender': generate_gender,
    'age': generate_age,
    'birth_date': generate_birth_date,
    'province': generate_province,
    'city': generate_city,
    'district': generate_district,
    'address': generate_address,
    'postcode': generate_postcode,
    'latitude': generate_latitude,
    'longitude': generate_longitude,
    'full_address': generate_full_address,
    'bank_card': generate_bank_card,
    'credit_card': generate_credit_card,
    'bank_name': generate_bank_name,
    'amount': generate_amount,
    'company_name': generate_company_name,
    'credit_code': generate_credit_code,
    'industry': generate_industry,
    'company_phone': generate_company_phone,
    'company_address': generate_company_address,
    'product_name': generate_product_name,
    'sku': generate_sku,
    'price': generate_price,
    'stock': generate_stock,
    'category': generate_category,
    'uuid': generate_uuid,
    'ip': generate_ip,
    'mac': generate_mac,
    'url': generate_url,
    'timestamp': generate_timestamp,
    'random_string': generate_random_string,
}


def get_generator(type_name: str):
    """根据类型名称获取对应的生成器函数"""
    if type_name not in GENERATOR_REGISTRY:
        raise ValueError(f"未知的生成器类型: {type_name}")
    return GENERATOR_REGISTRY[type_name]


def list_generators() -> list:
    """返回所有已注册的生成器类型名称列表"""
    return list(GENERATOR_REGISTRY.keys())
