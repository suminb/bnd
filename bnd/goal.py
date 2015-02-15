# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask.ext.login import login_required, current_user
from bnd.models import Goal, Team, Checkpoint, Evaluation
from bnd.forms import GoalForm
from bnd.utils import handle_request_type


goal_module = Blueprint(
    'goal', __name__, template_folder='templates/goal')


@goal_module.route('/view_all/ajax')
def view_all():
    team_id = request.args.get('team_id')
    checkpoint_id = request.args.get('checkpoint_id')
    goals = Goal.query.filter_by(team_id=team_id)
    checkpoint = Checkpoint.get_or_404(checkpoint_id)

    context = dict(
        goals=goals,
        checkpoint=checkpoint,
        team=checkpoint.team,
    )

    return render_template('goal/view_all_ajax.html', **context)


@goal_module.route('/<int:goal_id>')
@login_required
def view(goal_id):
    goal = Goal.get_or_404(goal_id)
    context = dict(
        goal=goal,
        team=current_user.current_team,
        checkpoint_id=request.args.get('checkpoint_id'),
    )
    return render_template('goal/view.html', **context)


@goal_module.route('/edit/new', methods=['get', 'post'], defaults=dict(goal_id=None))
@goal_module.route('/edit/<goal_id>', methods=['get', 'post'])
@login_required
def edit(goal_id):
    if goal_id is None:
        goal = Goal()
    else:
        goal = Goal.get_or_404(goal_id)

    form = GoalForm(request.form, obj=None)
    if form.validate_on_submit():
        form.populate_obj(goal)
        goal.user = current_user
        goal.team = current_user.current_team
        goal.save()

        return redirect(url_for('team.view', team_id=goal.team_id))

    context = dict(
        form=form,
        user=current_user,
    )
    return render_template('edit.html', **context)


# @handle_request_type
@goal_module.route('/<int:goal_id>/evaluate', methods=['get', 'post'])
@login_required
def evaluate(goal_id):
    def get():
        team_id, checkpoint_id = map(request.args.get,
                                     ['team_id', 'checkpoint_id'])

        goal = Goal.get_or_404(goal_id)
        checkpoint = Checkpoint.get_or_404(checkpoint_id)

        evaluation = Evaluation.query.filter_by(
            goal=goal,
            checkpoint=checkpoint,
        ).first()

        context = dict(
            goal=goal,
            checkpoint=checkpoint,
            evaluation=evaluation,
        )
        return render_template('goal/evaluate.html', **context)

    def post():
        team_id, checkpoint_id = map(request.args.get,
                                     ['team_id', 'checkpoint_id'])

        # TODO: Validate user input

        goal = Goal.get_or_404(goal_id)
        checkpoint = Checkpoint.get_or_404(checkpoint_id)

        evaluation = Evaluation.query.filter_by(
            goal=goal,
            checkpoint=checkpoint,
        ).first()

        if evaluation is None:
            evaluation = Evaluation()

        evaluation.user = current_user
        evaluation.goal = goal
        evaluation.checkpoint = checkpoint
        evaluation.evaluation = request.form.get('evaluation')

        evaluation.save()

        return redirect(url_for('goal.view', goal_id=goal_id, checkpoint_id=checkpoint.id))

    # FIXME: This is stupid
    return dict(get=get, post=post)[request.method.lower()]()