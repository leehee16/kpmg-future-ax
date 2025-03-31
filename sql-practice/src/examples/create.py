from ..database import execute_query

def create_table():
    """새로운 테이블을 생성합니다."""
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    execute_query(query)

def insert_user(name, email):
    """새로운 사용자를 추가합니다."""
    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    execute_query(query, (name, email)) 