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
        if current_user.has_current_team:
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


@curriculum_module.route('/checkpoint/<id>')
@login_required
def checkpoint(id):
    checkpoint = Checkpoint.get_or_404(id)
    context = dict(
        entity=checkpoint,
    )
    return render_template('curriculum/checkpoint.html', **context)


@curriculum_module.route('/goal/edit/new', methods=['get', 'post'], defaults=dict(id=None))
@curriculum_module.route('/goal/edit/<id>', methods=['get', 'post'])
@login_required
def goal_edit(id):
    if id is None:
        goal = Goal()
    else:
        goal = Goal.get_or_404(id)

    form = GoalForm(request.form, obj=None)
    if form.validate_on_submit():
        form.populate_obj(goal)
        goal.team = current_user.current_team
        goal.save()

        return redirect(url_for('curriculum.index'))

    context = dict(
        form=form,
        user=current_user,
    )
    return render_template('goal_edit.html', **context)


def curriculum_goal_evaluate():
    context = dict(
        user=current_user,
    )
    return render_template('goal_evaluate.html', **context)
