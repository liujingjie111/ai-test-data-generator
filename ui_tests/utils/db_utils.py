"""
数据库工具类
用于清理测试过程中产生的测试数据
"""
import sys
import os

# 添加 backend 目录到 Python 路径，并设置工作目录
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backend'))

# 确保工作目录是 backend 目录，这样数据库路径才能正确
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backend')
os.chdir(backend_dir)

from typing import List
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.template import Template


def get_db_session() -> Session:
    """
    获取数据库会话

    Returns:
        数据库会话对象
    """
    return SessionLocal()


def cleanup_test_templates() -> None:
    """
    清理测试模板（名称包含 "test" 或 "测试" 的模板）
    """
    db = get_db_session()
    try:
        # 查找并删除测试模板
        test_templates = db.query(Template).filter(
            (Template.name.like("%test%")) |
            (Template.name.like("%测试%"))
        ).all()

        for template in test_templates:
            db.delete(template)

        db.commit()
        print(f"已清理 {len(test_templates)} 条测试模板数据")

    except Exception as e:
        db.rollback()
        # 表不存在是正常情况，不需要报错
        if "no such table" not in str(e):
            print(f"清理测试数据失败: {str(e)}")
    finally:
        db.close()


def delete_template_by_name(name: str) -> bool:
    """
    根据名称删除模板

    Args:
        name: 模板名称

    Returns:
        是否删除成功
    """
    db = get_db_session()
    try:
        template = db.query(Template).filter(Template.name == name).first()
        if template:
            db.delete(template)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"删除模板失败: {str(e)}")
        return False
    finally:
        db.close()
