import os
from flask import Flask
from flask_session import Session
from config import Config
from routes.main_routes import main_bp
from routes.citizen_routes import citizen_bp
from routes.corp_routes import corp_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs("flask_session", exist_ok=True)

    # Server-side sessions
    Session(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(citizen_bp)
    app.register_blueprint(corp_bp)

    # Template filters
    from utils.helpers import format_datetime, time_ago
    app.jinja_env.filters["datetime"] = format_datetime
    app.jinja_env.filters["time_ago"] = time_ago

    @app.template_filter("status_class")
    def status_class(status):
        return {
            "pending": "status-pending",
            "in_progress": "status-progress",
            "resolved": "status-resolved",
            "escalated": "status-escalated",
            "closed": "status-closed"
        }.get(status, "status-pending")

    @app.template_filter("priority_class")
    def priority_class(priority):
        return {
            "low": "priority-low",
            "medium": "priority-medium",
            "high": "priority-high",
            "emergency": "priority-emergency"
        }.get(priority, "priority-medium")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
