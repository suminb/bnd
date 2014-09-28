from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Team
from bnd.forms import GoalForm
from functools import wraps


team_module = Blueprint(
    'team', __name__, template_folder='templates/team')


@team_module.route('/list')
def list_():
    teams = Team.query.all()
    context = dict(
        teams=teams,
    )
    return render_template('list.html', **context)


@team_module.route('/<int:id>')
def view(id):
    team = Team.get_or_404(id)
    context = dict(
        team=team,
    )
    return render_template('view.html', **context)


@team_module.route('/join/<id>')
def join(id):
    team = Team.get_or_404(id)
    context = dict(
        team=team,
    )
    return render_template('join.html', **context)
