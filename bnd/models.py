from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from bnd import app


db = SQLAlchemy(app)

if db.engine.driver != 'psycopg2':
    JSON = ARRAY = db.String


class CRUDMixin(object):
    """Copied from https://realpython.com/blog/python/python-web-applications-with-flask-part-ii/
    """  # noqa

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    # We will also proxy Flask-SqlAlchemy's get_or_44
    # for symmetry
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

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


class User(db.Model, UserMixin, CRUDMixin):
    __table_args__ = ( db.UniqueConstraint('oauth_provider', 'oauth_id'), {} )

    id = db.Column(db.Integer, primary_key=True)
    oauth_provider = db.Column(db.String, unique=True)
    oauth_id = db.Column(db.String, unique=True)
    given_name = db.Column(db.String)
    family_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    #: An enum name is required, otherwise the following error will be raised:
    #  sqlalchemy.exc.CompileError: Postgresql ENUM type requires a name.
    sex = db.Column(db.Enum('male', 'female', name='sex'))
    birthdate = db.Column(db.Date)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    data = db.Column(JSON)

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
        return []

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
    name = db.Column(db.String, unique=True)
    #: Long text to be shown when users are about to join a particular team
    poster = db.Column(db.Text)
    users = db.relationship('User', secondary=user_team_assoc,
        backref=db.backref('teams', lazy='dynamic'))
    checkpoints = db.relationship('Checkpoint', backref='team', lazy='dynamic')
    goals = db.relationship('Goal', backref='team', lazy='dynamic')


class Checkpoint(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    due_date = db.Column(db.DateTime(timezone=True))
    title = db.Column(db.String)
    # TODO: attendance
    evaluations = db.relationship('Evaluation', backref='checkpoint', lazy='dynamic')


class Goal(db.Model, CRUDMixin):
    """A goal contains multiple tasks."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    title = db.Column(db.String)
    content = db.Column(db.Text)
    criterion1 = db.Column(db.String)
    criterion2 = db.Column(db.String)
    criterion3 = db.Column(db.String)
    criterion4 = db.Column(db.String)
    # TODO: attendance
    evaluations = db.relationship('Evaluation', backref='goal', lazy='dynamic')


class Evaluation(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
    timestamp = db.Column(db.DateTime(timezone=True))
    evaluation1 = db.Column(db.Integer)
    evaluation2 = db.Column(db.Integer)
    evaluation3 = db.Column(db.Integer)
    evaluation4 = db.Column(db.Integer)


class Application(db.Model, CRUDMixin):
    """User application. Assumes the application cannot be modified once
    submitted."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime(timezone=True))
    data = db.Column(JSON)
