from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Checkpoint, Goal
from bnd.forms import GoalForm
from bnd.utils import handle_request_type


checkpoint_module = Blueprint(
    'checkpoint', __name__, template_folder='templates/checkpoint')


@checkpoint_module.route('/<int:checkpoint_id>')
def view(checkpoint_id):
    checkpoint = Checkpoint.get_or_404(checkpoint_id)
    context = dict(
        checkpoint=checkpoint,
    )
    return render_template('checkpoint/view.html', **context)
