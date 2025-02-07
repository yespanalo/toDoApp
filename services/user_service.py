from database import get_db_connection
from models.users import User

class UserService:
    @staticmethod
    def login(email, password):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return {"success": True, "message": "Login successful", "user": user}
        else:
            return {"success": False, "message": "Invalid credentials"}

    @staticmethod
    def get_all_users():
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT id, name, email, role FROM users")
            user_rows = cursor.fetchall()

            users = [User(id=row["id"], name=row["name"], email=row["email"], password=None, role=row["role"], created_at=None) for row in user_rows]

            return {"success": True, "message": "Users retrieved successfully", "users": [vars(user) for user in users]}

        except Exception as e:
            return {"success": False, "message": f"Error retrieving users: {str(e)}"}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
