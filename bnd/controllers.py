
from bnd import create_app
app = create_app(None)

from flask import request, render_template, redirect
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from bnd.forms import ApplicationForm
from bnd.models import db, User, Team, Checkpoint, Goal, Evaluation, Application





# FIXME: Refacfor the following section
def checkpoint_status_class(status):
    if status == 'Completed':
        return 'label-success'
    elif status == 'Past-due':
        return 'label-danger'
    else:
        return 'label-default'
app.jinja_env.globals.update(checkpoint_status_class=checkpoint_status_class)

admin = Admin(app)
classes = [User, Team, Checkpoint, Goal, Evaluation]
for cls in classes:
    admin.add_view(ModelView(cls, db.session, endpoint='admin_'+cls.__name__))

# See https://github.com/lepture/flask-oauthlib/blob/master/example/google.py
# for more examples


@app.route('/')
def index():
    context = dict(
    )

    return render_template('index.html', **context)


@app.route('/application', methods=['get', 'post'])
def application():
    form = ApplicationForm(request.form, obj=None)

    if form.validate_on_submit():
        Application.create(data=form.data)

        return redirect('/')

    context = dict(form=form)
    return render_template('application.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
