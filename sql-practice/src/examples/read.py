from ..database import fetch_all, fetch_one

def get_all_users():
    """모든 사용자를 조회합니다."""
    query = "SELECT * FROM users"
    return fetch_all(query)

def get_user_by_id(user_id):
    """ID로 사용자를 조회합니다."""
    query = "SELECT * FROM users WHERE id = %s"
    return fetch_one(query, (user_id,))

def get_user_by_email(email):
    """이메일로 사용자를 조회합니다."""
    query = "SELECT * FROM users WHERE email = %s"
    return fetch_one(query, (email,)) 