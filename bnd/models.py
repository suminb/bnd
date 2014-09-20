from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSON, ARRAY
from __init__ import app

db = SQLAlchemy(app)


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


class User(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
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


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)


user_team_assoc = db.Table(
    'user_team_assoc',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tasks = db.relationship('Task', backref='goal', lazy='dynamic')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))


class Application(db.Model, CRUDMixin):
    """User application. Assumes the application cannot be modified once
    submitted."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime(timezone=True))
    data = db.Column(JSON)
    #question1 = db.Column(db.String)
    #question2 = db.Column(db.String)
    #question3 = db.Column(db.Integer)
    #question4 = db.Column(db.Text)
    #question5 = db.Column(ARRAY(db.Integer))
