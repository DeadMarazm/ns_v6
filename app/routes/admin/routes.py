from flask import render_template
from flask_security import login_required, roles_required
from . import admin_bp

@admin_bp.route('/')
@login_required
@roles_required('admin')  # Ensures only admin users can access this route
def admin_home():
    return render_template('admin/index.html')
