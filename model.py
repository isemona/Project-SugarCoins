"""Models and database functions for SugarCoins project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions


class User(db.Model):
    """User of SugarCoin website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    gender_code = db.Column(db.String(1), db.ForeignKey('gender.gender_code'), index=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} gender_code={self.gender_code}>"



class Gender(db.Model):
    """Gender of user."""

    __tablename__ = "gender"

    gender_code = db.Column(db.String(1), nullable=True, primary_key=True) # nullable False gender is required
    allowance = db.Column(db.Integer, nullable=True) # can this be null? 

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Gender gender_code={self.gender_code} allowance={self.allowance}>"


class Weight(db.Model):
    '''Weight of user.'''

    __tablename__ = "weight"

    weight_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    current_weight = db.Column(db.Integer, nullable=True)
    date_time = db.Column(db.DateTime)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Weight weight_id={self.weight_id} current_weight={self.current_weight}>"

class Glucose(db.Model):
    '''Blood-glucose level of user.'''

    __tablename__ = "glucose"

    glucose_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    current_glucose = db.Column(db.Integer, nullable=True)
    date_time = db.Column(db.DateTime)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Glucose glucose_id={self.glucose_id} current_glucose={self.current_glucose}>"

class Food(db.Model):
    '''This table tracks food intake.'''

    food_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    food = db.Column(db.String(64), nullable=True) 
    cost = db.Column(db.Integer, nullable=True) # This will always change if you put it in the intake table, but here it is static

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Food food={self.food} cost={self.cost}>"


class Sugar(db.Model):
    '''Sugar intake of each user.'''

    __tablename__ = "sugar_intake"

    intake_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.food_id'), index=True)
    date_time = db.Column(db.DateTime)
    notes = db.Column(db.String(64), nullable=True) # FIX ME, IS THIS A DROP DOWN OPTION?

    food = db.relationship("Food", backref="intakes")
    user = db.relationship("User", backref="intakes")
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Sugar intake_id={self.intake_id} notes={self.notes}>"



#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sugarcoins'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)

    # you specified db.create_all() here to create the database no need to type this command on the terminal
    db.create_all()

    print("Connected to DB.")