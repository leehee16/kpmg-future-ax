import pymysql
from .config import MYSQL_CONFIG

def get_connection():
    """MySQL 데이터베이스 연결을 생성합니다."""
    return pymysql.connect(**MYSQL_CONFIG)

def execute_query(query, params=None):
    """SQL 쿼리를 실행합니다."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            conn.commit()
            return cursor

def fetch_all(query, params=None):
    """SELECT 쿼리의 결과를 모두 가져옵니다."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

def fetch_one(query, params=None):
    """SELECT 쿼리의 결과를 하나만 가져옵니다."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone() 