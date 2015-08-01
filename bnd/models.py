# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, current_user
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from bnd import redis_store
import click
import json


db = SQLAlchemy()

JsonType = db.String().with_variant(JSON(), 'postgresql')


def cached(func):
    """Cache data at a Redis store."""
    def wrapper(self, *args, **kwargs):
        key = 'func:{}-user:{}'.format(func.__name__, current_user.id)
        data = redis_store.get(key)

        if data is None:
            data = func(self, *args, **kwargs)
            redis_store.set(key, json.dumps(data))
        else:
            data = json.loads(data.decode('utf-8'))

        return data
    return wrapper


class CRUDMixin(object):
    """Copied from https://realpython.com/blog/python/python-web-applications-with-flask-part-ii/
    """  # noqa

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)

        if hasattr(instance, 'timestamp') \
                and getattr(instance, 'timestamp') is None:
            instance.timestamp = datetime.utcnow()

        return instance.save(commit=commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    # We will also proxy Flask-SqlAlchemy's get_or_44
    # for symmetry
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def exists(cls, **kwargs):
        row = cls.query.filter_by(**kwargs).first()
        return row is not None

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


user_team_assoc = db.Table(
    'user_team_assoc',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)


checkpoint_team_assoc = db.Table(
    'checkpoint_team_assoc',
    db.Column('checkpoint_id', db.Integer, db.ForeignKey('checkpoint.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)


class Announcement(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    db.Column(db.DateTime(timezone=False))
    title = db.Column(db.String)
    content = db.Column(db.Text)
    teams = db.relationship('Team', backref='announcement', lazy='dynamic')
    data = db.Column(JsonType)


class User(db.Model, UserMixin, CRUDMixin):
    __table_args__ = (db.UniqueConstraint('oauth_provider', 'oauth_id'), {})

    id = db.Column(db.Integer, primary_key=True)
    oauth_provider = db.Column(db.String)
    oauth_id = db.Column(db.String)
    given_name = db.Column(db.String)
    family_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    #: An enum name is required, otherwise the following error will be raised:
    #  sqlalchemy.exc.CompileError: Postgresql ENUM type requires a name.
    sex = db.Column(db.Enum('male', 'female', 'undisclosed', name='sex'))
    birthdate = db.Column(db.Date)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    zipcode = db.Column(db.String)

    #: URL of Google profile picture
    picture = db.Column(db.String)

    #: Arbitrary data
    data = db.Column(JsonType)

    goals = db.relationship('Goal', backref='user', lazy='dynamic')
    evaluations = db.relationship('Evaluation', backref='user', lazy='dynamic')

    def __repr__(self):
        return u'{}, {} <{}>'.format(
            self.family_name, self.given_name, self.email)

    def goals_for_team(self, team_id):
        return Goal.query.filter_by(user_id=self.id, team_id=team_id).all()

    def get_checkpoint_status(self, checkpoint):
        """Determines whether the user has an evaluation for a particular
        checkpoint."""

        evaluation = Evaluation.query \
            .filter_by(user_id=self.id, checkpoint_id=checkpoint.id).first()

        if evaluation is not None:
            return 'Completed'
        elif checkpoint.due_date is None:
            return 'Unknown'
        # elif checkpoint.due_date < datetime.now():
        #    return 'Past-due'
        # else:
        #    return 'In-progress'
        else:
            return 'Unknown'

    @property
    def name(self):
        # TODO: i18n
        return u'{}, {}'.format(self.family_name, self.given_name)

    @property
    def has_current_team(self):
        # FIXME: Determine whether the user currently belongs to any team based
        # on the timestamp
        return self.teams.count() > 0

    @property
    def current_team(self):
        """The current team to which the user belongs."""
        if self.has_current_team:
            return self.teams[0]  # FIXME: Return a proper team based on the current date
        else:
            raise Exception('User {} does not belong to any team'.format(self))

    @property
    def past_teams(self):
        raise NotImplementedError()

    def is_chair_of(self, team):
        return team.chair is not None and self.id == team.chair.id

    @staticmethod
    def get_by_oauth_id(oauth_id):
        return User.query.filter_by(oauth_id=oauth_id).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def check_email(email):
        """Check if there already exists a user having the specified email.
        :param email: An email address
        """
        user = User.query.filter_by(email=email).first()

        return user is not None


class Team(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    open_datetime = db.Column(db.DateTime(timezone=False))
    close_datetime = db.Column(db.DateTime(timezone=False))
    name = db.Column(db.String, unique=True)
    #: Long text to be shown when users are about to join a particular team
    classifier = db.Column(db.String)
    description = db.Column(db.Text)
    chair_id = db.Column(db.Integer, db.ForeignKey(User.id))
    chair = db.relationship(User, uselist=False)
    users = db.relationship('User', secondary=user_team_assoc,
                            backref=db.backref('teams', lazy='dynamic'))
    _checkpoints = db.relationship('Checkpoint',
                                   secondary=checkpoint_team_assoc,
                                   backref='team', lazy='dynamic')
    goals = db.relationship('Goal', backref='team', lazy='dynamic')

    def __repr__(self):
        return u"Team '{}'".format(self.name)

    @property
    def is_open(self):
        raise NotImplemented()

    @property
    def regular_checkpoints(self):
        return filter(lambda x: x.type != 'special', self.checkpoints)

    @property
    def checkpoints(self):
        from operator import attrgetter
        return sorted(self._checkpoints, key=attrgetter('due_date'))


class Checkpoint(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime(timezone=False))
    title = db.Column(db.String)
    description = db.Column(db.Text)
    type = db.Column(db.Enum('special', 'online', 'offline',
                             name='checkpoint_type'),
                     nullable=False, default='offline')

    evaluations = db.relationship('Evaluation', backref='checkpoint',
                                  lazy='dynamic')

    teams = db.relationship('Team', secondary=checkpoint_team_assoc,
                            backref='checkpoint', lazy='dynamic')

    def __repr__(self):
        return u"Checkpoint '{}'".format(self.title)

    @property
    def goals(self):
        """All goals which belong to this checkpoint."""
        return Goal.query.filter_by(team_id=self.team_id)

    def evaluations_for_user(self, user):
        return Evaluation.query.filter_by(user=user, checkpoint=self)

    def average_evaluation_for_user(self, user):
        average = Evaluation.query.with_entities(
            func.avg(Evaluation.score)
        ).filter_by(user=user, checkpoint=self).first()

        return average[0] if average[0] is not None else 0.0


class Goal(db.Model, CRUDMixin):
    """One evaluation per checkpoint"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    type = db.Column(db.Enum(u'전공', u'운동', u'예술', u'취미', u'생활',
                             u'기타', name='goal_type'),
                     nullable=False, default='offline')
    title = db.Column(db.String)
    content = db.Column(db.Text)
    criterion1 = db.Column(db.String)
    criterion2 = db.Column(db.String)
    criterion3 = db.Column(db.String)
    criterion4 = db.Column(db.String)
    # TODO: attendance
    evaluations = db.relationship('Evaluation', backref='goal', lazy='dynamic')

    def __repr__(self):
        return u"Goal '{}'".format(self.title)


class Evaluation(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
    timestamp = db.Column(db.DateTime(timezone=False))
    score = db.Column(db.Integer)
    data = db.Column(JsonType)

    @staticmethod
    def fetch(user_id, checkpoint_id, goal_id):
        return Evaluation.query\
            .filter(
                Evaluation.user_id == user_id,
                Evaluation.checkpoint_id == checkpoint_id,
                Evaluation.goal_id == goal_id)\
            .first()


class CheckpointEvaluation(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
    timestamp = db.Column(db.DateTime(timezone=False))
    data = db.Column(JsonType)


# FIXME: To be relocated to elsewhere
class EvaluationChart(object):
    def extract_user_data(self, user, checkpoint_ids):

        # FIXME: Potential risk of SQL injection
        raw_query = """
        SELECT title, checkpoint.id, goal_id, score FROM checkpoint LEFT JOIN (
            SELECT checkpoint_id, goal_id, avg(score) AS score FROM evaluation
            WHERE user_id={0}
            GROUP BY checkpoint_id, goal_id
        ) AS evaluations ON checkpoint.id=evaluations.checkpoint_id
        WHERE checkpoint.id IN ({1})
        """.format(user.id, ','.join(map(str, checkpoint_ids)))

        # inner_query = Evaluation.query.with_entities(
        #     Evaluation.checkpoint_id, func.avg(Evaluation.score)
        # ).filter(
        #     Evaluation.user_id==user.id
        # ).group_by(
        #     Evaluation.checkpoint_id
        # ).subquery()
        #
        # user_evaluations = Checkpoint.query.outerjoin(
        #     inner_query.alias('evaluation'), Evaluation.checkpoint_id==Checkpoint.id
        # ).filter(
        #     Checkpoint.id.in_(checkpoint_ids)
        # )

        return db.engine.execute(raw_query)

        # return user_evaluations.all()

    def get_user_data(self, user, team):
        """
        :param user:
        :param team:

        :type user: User
        :type team: Team

        :return: A dictionary containing user evaluation data for each goal
        """
        checkpoint_ids = [c.id for c in team.regular_checkpoints]
        goals = [g for g in self.get_current_goals(user)]

        evals = {}

        # For each goal,
        for index, goal in enumerate(goals):
            evals[goal.id] = {}

            for checkpoint_id in checkpoint_ids:
                evals[goal.id][checkpoint_id] = 0.0

            for checkpoint_id, score in \
                    self.get_user_evaluations_for_goal(user, goal):
                evals[goal.id][checkpoint_id] = score

        return evals

    def extract_team_data(self, team):

        user_ids = [u.id for u in team.users]

        team_evaluations = Evaluation.query.with_entities(
            func.avg(Evaluation.score)
        ).filter(
            Evaluation.user_id.in_(user_ids)
        ).group_by(
            Evaluation.checkpoint_id
        ).group_by(
            Evaluation.goal_id
        )

        return team_evaluations.all()

    def get_current_goals(self, user):
        goals = Goal.query.filter(
            Goal.user_id == user.id,
            Goal.team_id == user.current_team.id,
        )
        return goals.all()

    def get_user_evaluations_for_goal(self, user, goal):
        evaluations = Evaluation.query.with_entities(
            Evaluation.checkpoint_id,
            func.avg(Evaluation.score)
        ).filter(
            Evaluation.user_id == user.id, Evaluation.goal_id == goal.id
        ).group_by(
            Evaluation.checkpoint_id
        )
        return [(int(x[0]), float(x[1])) for x in evaluations.all()]

    @cached
    def get_chart_data(self, user, team):
        """Outputs data to feed to a chart library."""

        labels = [(c.id, c.title) for c in team.regular_checkpoints]

        goal_ids = [g.id for g in self.get_current_goals(user)]

        user_data = self.get_user_data(user, team)

        arrays = [None] * (len(goal_ids) + 1)

        # First element is a list of labels
        arrays[0] = labels

        for index, goal_id in enumerate(goal_ids):
            arrays[index + 1] = []

            for checkpoint_id, label in labels:
                arrays[index + 1].append(user_data[goal_id][checkpoint_id])

        return arrays


@click.group()
def cli():
    return None


@cli.command()
def create_all():
    from bnd import create_app
    app = create_app(__name__)
    with app.app_context():
        db.create_all()


@cli.command()
def drop_all():
    from bnd import create_app
    app = create_app(__name__)
    with app.app_context():
        db.drop_all()



if __name__ == '__main__':
    cli()
