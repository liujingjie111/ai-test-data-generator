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
from app.utils.data_generators.registry import (
    GENERATOR_REGISTRY,
    get_generator,
    list_generators,
)
