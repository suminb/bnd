from . import app


def test_pages(app):
    testapp = app.test_client()
    pages = ('/', '/user/login', '/curriculum')

    for page in pages:
        resp = testapp.get(page)
        assert resp.status_code != 404


def test_non_existing_pages(app):
    testapp = app.test_client()

    resp = testapp.get('/this-page-should-not-exist')
    assert resp.status_code == 404

    resp = testapp.post('/this-page-should-not-exist-either')
    assert resp.status_code == 404


# def test_login_required_pages(app):
#     testapp = app.test_client()
#
#     pages = ('/curriculum', '/user/info')
#
#     for page in pages:
#         resp = testapp.get(page)
#         # The app is set to redirect to /login when @login_required decorator
#         # is present
#         assert resp.status_code == 302
