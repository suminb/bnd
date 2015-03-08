"""THIS MODULE IS DEPRECATED"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Checkpoint, Goal
from bnd.forms import GoalForm
from functools import wraps


curriculum_module = Blueprint(
    'curriculum', __name__, template_folder='templates/curriculum')


def redirect_to_join_team():
    return redirect('/team/list')

def team_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_anonymous() and current_user.has_current_team:
            return func(*args, **kwargs)
        else:
            return redirect_to_join_team()

    return decorated_view

@curriculum_module.route('')
@login_required
@team_required
def index():
    context = dict(
        user=current_user,
    )
    return render_template('index.html', **context)
