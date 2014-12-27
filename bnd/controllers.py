
from bnd import create_app
app = create_app(None)


# FIXME: Refacfor the following section
def checkpoint_status_class(status):
    if status == 'Completed':
        return 'label-success'
    elif status == 'Past-due':
        return 'label-danger'
    else:
        return 'label-default'


if __name__ == '__main__':
    app.jinja_env.globals.update(checkpoint_status_class=checkpoint_status_class)
    app.run(host='0.0.0.0', debug=True)
