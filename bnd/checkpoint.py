from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Checkpoint


checkpoint_module = Blueprint(
    'checkpoint_module', __name__, template_folder='templates/checkpoint')


@checkpoint_module.route('/<int:id>')
def view(id):
    checkpoint = Checkpoint.get_or_404(id)
    context = dict(
        checkpoint=checkpoint,
    )
    return render_template('view.html', **context)
