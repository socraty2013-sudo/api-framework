import pytest
from common.db_handler import DBHandler

@pytest.fixture()
def db():
    """直接操作数据库"""
    return DBHandler()