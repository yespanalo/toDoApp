from database import get_db_connection
from models.projects import Projects

class ProjectsService:
    @staticmethod
    def get_all_projects():
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM projects")
            projects = cursor.fetchall()
            return {"success": True, "message": "Projects retrieved successfully", "projects": projects}
        except Exception as e:
            return {"success": False, "message": f"Error retrieving projects: {str(e)}"}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    @staticmethod
    def get_project_by_id(project_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Query for a specific project by ID
            cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
            project = cursor.fetchone()

            if project:
                return {"success": True, "message": "Project retrieved successfully", "project": project}
            else:
                return {"success": False, "message": "Project not found"}

        except Exception as e:
            return {"success": False, "message": f"Error retrieving project: {str(e)}"}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    @staticmethod
    def create_project(name, description, created_by):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if the project name already exists
            cursor.execute("SELECT COUNT(*) FROM projects WHERE name = %s", (name,))
            (count,) = cursor.fetchone()

            if count > 0:
                return {"success": False, "message": "Project name already exists"}

            # Insert new project
            cursor.execute(
                "INSERT INTO projects (name, description, created_by) VALUES (%s, %s, %s)", 
                (name, description, created_by)
            )
            conn.commit()
            return {"success": True, "message": "Project created successfully"}

        except Exception as e:
            return {"success": False, "message": f"Error creating project: {str(e)}"}

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


