from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Checkpoint, Goal
from bnd.forms import GoalForm


checkpoint_module = Blueprint(
    'checkpoint', __name__, template_folder='templates/checkpoint')


@checkpoint_module.route('/<int:checkpoint_id>')
def view(checkpoint_id):
    checkpoint = Checkpoint.get_or_404(checkpoint_id)
    context = dict(
        checkpoint=checkpoint,
    )
    return render_template('checkpoint/view.html', **context)


@checkpoint_module.route('/<int:checkpoint_id>/goal/<int:goal_id>')
@login_required  # TODO: Maybe we should make a @ajax_login_required decorator
def goal_view(checkpoint_id, goal_id):
    context = dict()
    return render_template('checkpoint/ajax_view_goal.html', **context)


@checkpoint_module.route('/<int:checkpoint_id>/goal/new', defaults=dict(goal_id='new'))
@checkpoint_module.route('/checkpoint/<int:checkpoint_id>/goal/<int:goal_id>/edit', methods=['get', 'post'])
@login_required
def goal_edit(checkpoint_id, goal_id):

    checkpoint = Checkpoint.get_or_404(checkpoint_id)

    if goal_id == 'new':
        goal = Goal()
    else:
        goal = Goal.get_or_404(id)

    form = GoalForm(request.form, obj=None)
    if form.validate_on_submit():
        form.populate_obj(goal)
        goal.user = current_user
        goal.team = current_user.current_team
        goal.save()

        return '', 200

    context = dict(
        checkpoint=checkpoint,
        form=form,
        team=checkpoint.team,
        goal=goal,
        user=current_user,
    )
    return render_template('goal_edit.html', **context)


@checkpoint_module.route('/<int:checkpoint_id>/goal/<int:goal_id>/evaluate', methods=['post'])
@login_required
def evaluate(checkpoint_id, goal_id):
    return '', 200