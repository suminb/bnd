from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from bnd.models import Team, Checkpoint, Goal
from bnd.forms import GoalForm

from flask import request, render_template, redirect
from bnd.models import db, User, Team, Checkpoint, Goal, Evaluation

main_module = Blueprint(
    'main', __name__, template_folder='templates/main')


@main_module.route('/')
def index():
    context = dict(
    )
    return render_template('index.html', **context)
