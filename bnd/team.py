from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Team, Checkpoint, Goal, EvaluationChart
from bnd.forms import GoalForm


team_module = Blueprint(
    'team', __name__, template_folder='templates/team')


@team_module.route('/view_all')
def view_all():
    teams = Team.query.all()
    context = dict(
        teams=teams,
    )
    return render_template('view_all.html', **context)


@team_module.route('/<int:team_id>')
@login_required
def view(team_id):
    team = Team.get_or_404(team_id)

    context = dict(
        team=team,
    )
    return render_template('team/view.html', **context)


@team_module.route('/<int:team_id>/progress')
@login_required
def progress(team_id):
    team = Team.get_or_404(team_id)

    chart_data = EvaluationChart().get_chart_data(current_user, team)

    context = dict(
        team=team,
        chart_labels=chart_data[0],
        chart_user_evaluations=chart_data[1],
    )
    return render_template('team/progress.html', **context)


@team_module.route('/<int:team_id>/members')
@login_required
def members(team_id):
    team = Team.get_or_404(team_id)

    # TODO: Make a decorator to do this
    if not current_user.is_chair_of(team):
        return u'{} is not the chair of {}'.format(current_user, team), 403

    context = dict(
        team=team,
        members=team.users,
    )
    return render_template('team/members.html', **context)

@team_module.route('/join/<int:team_id>')
def join(team_id):
    team = Team.get_or_404(team_id)
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
        goal.user = current_user
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
