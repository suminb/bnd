from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Goal
from bnd.forms import GoalForm

goal_module = Blueprint(
    'goal', __name__, template_folder='templates/goal')


@goal_module.route('/<int:id>')
def view(id):
    goal = Goal.get_or_404(id)
    context = dict(
        goal=goal,
    )
    return render_template('view.html', **context)


@goal_module.route('/edit/new', methods=['get', 'post'], defaults=dict(id=None))
@goal_module.route('/edit/<id>', methods=['get', 'post'])
@login_required
def edit(id):
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
    return render_template('edit.html', **context)


