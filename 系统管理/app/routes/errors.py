from flask import Blueprint, render_template

errors_bp = Blueprint('errors', __name__)

@errors_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@errors_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

@errors_bp.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403