from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Checkpoint, Team, Goal, Evaluation
from bnd.forms import GoalForm
from bnd.utils import handle_request_type
import re


checkpoint_module = Blueprint(
    'checkpoint', __name__, template_folder='templates/checkpoint')


@checkpoint_module.route('/<int:checkpoint_id>')
@login_required
def view(checkpoint_id):
    team_id, goal_id = map(request.args.get,
                             ['team_id', 'goal_id'])

    checkpoint = Checkpoint.get_or_404(checkpoint_id)
    team = Team.get_or_404(team_id)
    goals = Goal.query.filter_by(team_id=team.id, user_id=current_user.id)

    context = dict(
        checkpoint=checkpoint,
        team=team,
        goals=goals,
    )
    return render_template('checkpoint/view.html', **context)


@checkpoint_module.route('/<int:checkpoint_id>/evaluate', methods=['POST'])
@login_required
def evaluate(checkpoint_id):
    team_id = request.args.get('team_id')

    checkpoint = Checkpoint.get_or_404(checkpoint_id)
    team = Team.get_or_404(team_id)

    # TODO: Deal with multiple goals

    for k, v in request.form.items():
        m = re.match(r'goal-(?P<goal_id>\d+)', k)

        if m is not None:
            goal_id = m.group('goal_id')
            Evaluation.create(
                evaluation=v,
                user=current_user,
                checkpoint=checkpoint,
                goal_id=goal_id,
            )

    context = dict(
        checkpoint=checkpoint,
        team=team,
    )
    return redirect(url_for('checkpoint.view', checkpoint_id=checkpoint.id, team_id=team.id))