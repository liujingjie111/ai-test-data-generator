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
    清理所有测试模板数据
    匹配规则：名称包含中文"测试"、英文"test"、"(copy)"，或所有在 TEMPLATE_NAMES 中定义的模板名称
    """
    db = get_db_session()
    try:
        # 所有需要清理的模板名称模式
        filter_conditions = [
            Template.name.like("%测试%"),
            Template.name.like("%test%"),
            Template.name.like("%(copy)%"),
            Template.name.like("%待删除%"),
            Template.name.like("%待复制%"),
            Template.name.like("%待编辑%"),
            Template.name.like("%已编辑%"),
            Template.name.like("%编辑取消%"),
            Template.name.like("%多字段%"),
            Template.name.like("%用于生成%"),
        ]

        # 组合查询条件（OR）
        from sqlalchemy import or_
        test_templates = db.query(Template).filter(or_(*filter_conditions)).all()

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
