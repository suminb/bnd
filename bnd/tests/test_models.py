from . import app, db


def test_team_chair(app, db):
    from bnd.models import User, Team
    import random

    def create_entities():
        user = User.create(
            oauth_provider='Unknown', oauth_id=random.randint(0, 1000000),
            family_name='Fox', given_name='Megan', email='fox@megan.com')

        Team.create(chair_id=user.id)
        Team.create()

    with app.app_context():

        create_entities()

        user = User.get(1)
        team1, team2 = Team.get(1), Team.get(2)

        assert user.is_chair_of(team1) is True
        assert user.is_chair_of(team2) is False