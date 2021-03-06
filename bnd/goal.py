# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Goal, Checkpoint, Evaluation
from bnd.forms import GoalForm


goal_module = Blueprint(
    'goal', __name__, template_folder='templates/goal')


@goal_module.route('/')
@login_required
def index():
    team = current_user.current_team
    goals = Goal.query.filter_by(user_id=current_user.id, team_id=team.id)
    context = dict(
        team=team,
        goals=goals,
    )
    return render_template('goal/index.html', **context)


@goal_module.route('/<int:goal_id>', methods=['get'])
@login_required
def view(goal_id):
    goal = Goal.get_or_404(goal_id)
    context = dict(
        goal=goal,
        team=current_user.current_team,
        checkpoint_id=request.args.get('checkpoint_id'),
    )
    return render_template('goal/view.html', **context)


@goal_module.route('/<int:goal_id>', methods=['delete'])
@login_required
def delete(goal_id):
    goal = Goal.get_or_404(goal_id)

    Evaluation.query.filter(Evaluation.goal_id == goal.id).delete()
    goal.delete()

    return ''


@goal_module.route('/edit/new', methods=['get', 'post'],
                   defaults=dict(goal_id=None))
@goal_module.route('/edit/<goal_id>', methods=['get', 'post'])
@login_required
def edit(goal_id):
    checkpoint_id = request.args.get('checkpoint_id')

    if goal_id is None:
        goal = Goal()
    else:
        goal = Goal.get_or_404(goal_id)

    form = GoalForm(request.form, obj=goal)
    if form.validate_on_submit():
        form.populate_obj(goal)
        goal.user = current_user
        goal.team = current_user.current_team
        goal.save()

        return redirect(url_for('goal.index', checkpoint_id=checkpoint_id,
                                team_id=goal.team_id))

    context = dict(
        form=form,
        goal=goal,
        user=current_user,
    )
    return render_template('edit.html', **context)
