from flask import Flask
from controllers.user_controller import user_bp
from controllers.project_controller import projects_bp
from controllers.taks_controller import tasks_bp
from controllers.priorities_controller import priorities_bp
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(priorities_bp)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
