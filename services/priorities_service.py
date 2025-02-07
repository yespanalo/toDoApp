from database import get_db_connection
from models.priorities import Priorities

class PrioritiesService:
    @staticmethod
    def get_all_priorities():
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM priorities")
            priority_rows = cursor.fetchall()
            
            # Convert rows into Priorities objects
            priorities = [Priorities(**row) for row in priority_rows]

            # Convert objects into dictionaries before returning
            return {
                "success": True,
                "message": "Priorities retrieved successfully",
                "priorities": [vars(priority) for priority in priorities]  
            }

        except Exception as e:
            return {"success": False, "message": f"Error retrieving priorities: {str(e)}"}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
