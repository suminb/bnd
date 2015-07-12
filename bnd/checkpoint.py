from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Checkpoint, Team, Goal, Evaluation, \
    CheckpointEvaluation,db
from datetime import datetime
import re


checkpoint_module = Blueprint(
    'checkpoint', __name__, template_folder='templates/checkpoint')


@checkpoint_module.route('/<int:checkpoint_id>')
@login_required
def view(checkpoint_id):
    team_id, goal_id = map(request.args.get, ['team_id', 'goal_id'])

    checkpoint = Checkpoint.get_or_404(checkpoint_id)
    team = Team.get_or_404(team_id)
    goals = Goal.query.filter_by(team_id=team.id, user_id=current_user.id)

    evaluations = {}
    # FIXME: Revise the following section; use a JOIN statement
    for goal in goals:
        evaluations[goal.id] = Evaluation.fetch(current_user.id,
                                                checkpoint.id, goal.id)

    context = dict(
        checkpoint=checkpoint,
        team=team,
        goals=goals,
        evaluations=evaluations,
    )
    return render_template('checkpoint/view.html', **context)


@checkpoint_module.route('/<int:checkpoint_id>/evaluate', methods=['POST'])
@login_required
def evaluate(checkpoint_id):
    """This will be called when a user clicks a submit button on the
    checkpoint.view page."""

    team_id = request.args.get('team_id')

    checkpoint = Checkpoint.get_or_404(checkpoint_id)
    team = Team.get_or_404(team_id)

    # Process CheckpointEvaluation first
    attendance = request.form.get('attendance', 'na')
    essay = request.form.get('essay', 'na')
    data = dict(attendance=attendance, essay=essay)

    checkpoint_evaluation = CheckpointEvaluation.query.filter_by(
        user_id=current_user.id,
        checkpoint_id=checkpoint.id,
    ).first()

    if checkpoint_evaluation is None:
        CheckpointEvaluation.create(
            user_id=current_user.id,
            checkpoint_id=checkpoint.id,
            data=data,
        )
    else:
        checkpoint_evaluation.timestamp = datetime.utcnow()
        checkpoint_evaluation.data = data
        db.session.commit()

    # Then process Evaluation
    for k, v in request.form.items():
        m = re.match(r'goal-(?P<goal_id>\d+)', k)

        if m is not None:
            goal_id = m.group('goal_id')

            evaluation = Evaluation.query.filter_by(
                user_id=current_user.id,
                checkpoint_id=checkpoint.id,
                goal_id=goal_id).first()

            if evaluation is None:
                Evaluation.create(
                    score=v,
                    user=current_user,
                    checkpoint=checkpoint,
                    goal_id=goal_id,
                )
            else:
                evaluation.timestamp = datetime.utcnow()
                evaluation.score = v
                db.session.commit()

    return redirect(url_for('checkpoint.view', checkpoint_id=checkpoint.id,
                            team_id=team.id))
