from bnd import app
import pytest


HOST = 'http://localhost:5000'


@pytest.fixture(scope='module')
def testapp():
    """ setup any state specific to the execution of the given module."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' # FIXME: Use tempfile
    client = app.test_client()

    from bnd.models import db
    db.create_all()

    return client


def test_pages(testapp):
    pages = ('',)

    for page in pages:
        resp = testapp.get('/')
        assert resp is not None
