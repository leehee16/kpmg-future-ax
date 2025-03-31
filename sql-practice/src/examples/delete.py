from ..database import execute_query

def delete_user(user_id):
    """사용자를 삭제합니다."""
    query = "DELETE FROM users WHERE id = %s"
    execute_query(query, (user_id,))

def delete_all_users():
    """모든 사용자를 삭제합니다."""
    query = "DELETE FROM users"
    execute_query(query) 