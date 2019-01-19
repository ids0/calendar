from flask import Blueprint, render_template

errorsAPP = Blueprint("errors", __name__)

@errorsAPP.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@errorsAPP.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errorsAPP.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500