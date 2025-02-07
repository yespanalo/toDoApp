from database import get_db_connection
from models.task import Tasks

class TaskService:
    @staticmethod
    def get_all_tasks():
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary = True)
            cursor.execute ("SELECT * FROM tasks")
            task_rows = cursor.fetchall()

            # Convert each row into a Tasks object
            tasks = [Tasks(**row) for row in task_rows]
            return {"success": True , "message": "Tasks retrieved successfully", "projects": tasks}
        except Exception as e:
            return {"success": False, "message": f"Error retrieving tasks: {str(e)}"}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_task_by_id(project_id, status_id=None):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
            SELECT t.*, s.name AS status_name
            FROM tasks t
            LEFT JOIN statuses s ON t.status_id = s.id
            WHERE t.project_id = %s
            """

            # Parameters list (start with project_id)
            params = [project_id]

            # Add status_id filter only if status_id is NOT 0
            if status_id and status_id != 0:
                query += " AND t.status_id = %s"
                params.append(status_id)

            cursor.execute(query, tuple(params))
            task = cursor.fetchall()

            if task:
                return {"success": True, "message": "Task retrieved successfully", "tasks": task}
            else:
                return {"success": False, "message": "No tasks found", "tasks": []}

        except Exception as e:
            return {"success": False, "message": f"Error retrieving project: {str(e)}"}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    @staticmethod
    def get_task_by_task_id(task_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
            SELECT t.*, s.name AS status_name
            FROM tasks t
            LEFT JOIN statuses s ON t.status_id = s.id
            WHERE t.id = %s
            """

            cursor.execute(query, (task_id,))
            task = cursor.fetchone()  # Fetch a single task

            if task:
                return {"success": True, "message": "Task retrieved successfully", "task": task}
            else:
                return {"success": False, "message": "Task not found", "task": None}

        except Exception as e:
            return {"success": False, "message": f"Error retrieving task: {str(e)}"}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    
    @staticmethod
    def create_task(title, description, project_id, assigned_to, priority_id, created_by):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Fix: Ensure (title,) is a tuple
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE title = %s", (title,))
            (count,) = cursor.fetchone()

            if count > 0:
                return {"success": False, "message": "Task title already exists"}

            cursor.execute(
                "INSERT INTO tasks (title, description, project_id, assigned_to, status_id, priority_id, created_by) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (title, description, project_id, assigned_to, 4, priority_id, created_by)
            )
            conn.commit()

            return {"success": True, "message": "Task created successfully"}

        except Exception as e:
            return {"success": False, "message": f"Error creating task: {str(e)}"}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def update_task(task_id, title=None, description=None, assigned_to=None, priority_id=None):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if the task exists
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE id = %s", (task_id,))
            (count,) = cursor.fetchone()

            if count == 0:
                return {"success": False, "message": "Task not found"}

            # Build dynamic update query
            updates = []
            params = []

            if title:
                updates.append("title = %s")
                params.append(title)
            if description:
                updates.append("description = %s")
                params.append(description)
            if assigned_to:
                updates.append("assigned_to = %s")
                params.append(assigned_to)
            if priority_id:
                updates.append("priority_id = %s")
                params.append(priority_id)

            if not updates:
                return {"success": False, "message": "No fields provided for update"}

            # Add task_id to parameters for the WHERE clause
            params.append(task_id)

            query = f"UPDATE tasks SET {', '.join(updates)}, updated_at = NOW() WHERE id = %s"
            cursor.execute(query, tuple(params))
            conn.commit()

            return {"success": True, "message": "Task updated successfully"}

        except Exception as e:
            return {"success": False, "message": f"Error updating task: {str(e)}"}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()






