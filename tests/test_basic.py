from bnd import create_app
import pytest


HOST = 'http://localhost:5000'


@pytest.fixture(scope='session')
def testapp():
    """ setup any state specific to the execution of the given module."""
    app = create_app(None)
    client = app.test_client()

    from bnd.models import db
    with app.app_context():
        db.create_all()

    return client


def test_pages(testapp):
    pages = ('/', '/user/login', '/curriculum')

    for page in pages:
        resp = testapp.get(page)
        assert resp.status_code != 404


def test_non_existing_pages(testapp):
    resp = testapp.get('/this-page-should-not-exist')
    assert resp.status_code == 404

    resp = testapp.post('/this-page-should-not-exist-either')
    assert resp.status_code == 404


def test_login_required_pages(testapp):
    pages = ('/curriculum', '/user/info')

    for page in pages:
        resp = testapp.get(page)
        # The app is set to redirect to /login when @login_required decorator
        # is present
        assert resp.status_code == 302
