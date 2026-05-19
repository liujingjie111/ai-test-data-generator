import secrets
from app.database import SessionLocal
from app.models.api_key import ApiKey

# 生成API密钥
generated_key = f"sk-{secrets.token_hex(32)}"

db = SessionLocal()
try:
    db_api_key = ApiKey(
        key=generated_key,
        name="临时调试密钥",
        is_active=True,
        expires_at=None,
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    
    print("=" * 60)
    print("API密钥创建成功！")
    print(f"密钥ID: {db_api_key.id}")
    print(f"密钥名称: {db_api_key.name}")
    print(f"密钥值: {generated_key}")
    print("=" * 60)
    print("请复制上面的密钥并在前端使用")
finally:
    db.close()
