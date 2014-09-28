from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Team, Checkpoint, Goal
from bnd.forms import GoalForm


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


@team_module.route('/<int:team_id>/checkpoint/<int:checkpoint_id>')
@login_required
def checkpoint_view(team_id, checkpoint_id):
    team = Team.get_or_404(team_id)
    checkpoint = Checkpoint.get_or_404(checkpoint_id)
    context = dict(
        team=team,
        checkpoint=checkpoint,
    )
    return render_template('/checkpoint_view.html', **context)


@team_module.route(
    '/<int:team_id>/goal/new',
    methods=['get', 'post'],
    defaults=dict(goal_id='new'))
@team_module.route(
    '/<int:team_id>/goal/<int:goal_id>/edit',
    methods=['get', 'post'])
@login_required
def goal_edit(team_id, goal_id):

    team = Team.get_or_404(team_id)

    if goal_id == 'new':
        goal = Goal()
    else:
        goal = Goal.get_or_404(id)

    form = GoalForm(request.form, obj=None)
    if form.validate_on_submit():
        form.populate_obj(goal)
        goal.team = current_user.current_team
        goal.save()

        return redirect(url_for('team.view', id=team_id))

    context = dict(
        form=form,
        team=team,
        goal=goal,
        user=current_user,
    )
    return render_template('goal_edit.html', **context)


