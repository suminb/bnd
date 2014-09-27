from flask import Blueprint, render_template
from flask.ext.login import login_required, current_user

curriculum_module = Blueprint('curriculum', __name__, template_folder='templates')


@curriculum_module.route('/')
@login_required
def curriculum():
    context = dict(
        user=current_user,
    )
    return render_template('curriculum.html', **context)


