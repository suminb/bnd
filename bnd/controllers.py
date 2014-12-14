
from bnd import create_app


# FIXME: Refacfor the following section
def checkpoint_status_class(status):
    if status == 'Completed':
        return 'label-success'
    elif status == 'Past-due':
        return 'label-danger'
    else:
        return 'label-default'

# See https://github.com/lepture/flask-oauthlib/blob/master/example/google.py
# for more examples


if __name__ == '__main__':
    app = create_app(None)
    app.jinja_env.globals.update(checkpoint_status_class=checkpoint_status_class)
    app.run(host='0.0.0.0', debug=True)
