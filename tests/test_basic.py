from bnd.controllers import app
import pytest


HOST = 'http://localhost:5000'


@pytest.fixture(scope='module')
def testapp():
    """ setup any state specific to the execution of the given module."""
    client = app.test_client()

    from bnd.models import db
    db.create_all()

    return client


def test_pages(testapp):
    pages = ('/', '/curriculum')

    for page in pages:
        resp = testapp.get(page)
        assert resp.status_code != 404
