from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Checkpoint, Team, Goal
from bnd.forms import GoalForm
from bnd.utils import handle_request_type


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
