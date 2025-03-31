from ..database import execute_query

def update_user_name(user_id, new_name):
    """사용자의 이름을 업데이트합니다."""
    query = "UPDATE users SET name = %s WHERE id = %s"
    execute_query(query, (new_name, user_id))

def update_user_email(user_id, new_email):
    """사용자의 이메일을 업데이트합니다."""
    query = "UPDATE users SET email = %s WHERE id = %s"
    execute_query(query, (new_email, user_id)) 