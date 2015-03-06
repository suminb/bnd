from bnd import create_app
import pytest
import os

def setup_module(module):
    """ setup any state specific to the execution of the given module."""


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    os.unlink('bnd/test.db')

@pytest.fixture(scope='function')
def testapp():
    """ setup any state specific to the execution of the given module."""
    app = create_app(None, db_uri='sqlite:///test.db')
    client = app.test_client()

    from bnd.models import db
    with app.app_context():
        db.create_all()

    return client


def test_team_chair(testapp):
    """TODO: Move this function elsewhere."""

    from bnd.models import User, Team
    import random

    def create_entities():
        user = User.create(
            oauth_provider='Unknown', oauth_id=random.randint(0, 1000000),
            family_name='Fox', given_name='Megan', email='fox@megan.com')

        Team.create(chair_id=user.id)
        Team.create()

    with testapp.application.app_context():

        create_entities()

        user = User.get(1)
        team1, team2 = Team.get(1), Team.get(2)

        assert user.is_chair_of(team1) is True
        assert user.is_chair_of(team2) is False