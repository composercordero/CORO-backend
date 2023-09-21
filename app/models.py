import os
import base64
from app import db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

# CONDUCTOR (USER) -------------------------------------------------

class Conductor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String, nullable = False)
    username = db.Column(db.String(75), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    token = db.Column(db.String(32), index = True, unique = True)
    token_expiration = db.Column(db.DateTime)
    organization = db.relationship('Organization', backref = 'author', cascade = 'delete')
    programs = db.relationship('Program', backref = 'conductor')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password'))

    def __repr__(self):
        return f"< Conductor {self.id} | {self.username} >"
    
    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)
    
    def get_token(self, expires_in=7200):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds = 60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds = expires_in)
        db.session.commit()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds = 1)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'username': self.username,
            'token expiration': self.token_expiration
        }

    @login.user_loader
    def load_user(user_id):
        return db.session.get(Conductor, user_id)
    
# ORGANIZATION -------------------------------------------------

class Organization(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String, nullable = False)
    website = db.Column(db.String(75), nullable = False, unique = True)
    conductor_id = db.Column(db.Integer, db.ForeignKey('conductor.id')) 
    choir = db.relationship('Choir', backref = 'organization', cascade = 'delete')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Organization {self.id} | {self.name} >"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
        }

# CHOIR -------------------------------------------------

    
class Choir(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = False)
    hymns = db.relationship('Hymn', backref = 'choir', cascade = 'delete')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Choir {self.id} | {self.address_one} >"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

# ADDRESS -------------------------------------------------

class Address(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    address_one = db.Column(db.String(100), nullable = False)
    address_two = db.Column(db.String(100))
    city = db.Column(db.String(30), nullable = False)
    state = db.Column(db.String(30), nullable = False)
    zip_code = db.Column(db.String(10), nullable = False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Address {self.id} | {self.address_one} >"

    def to_dict(self):
        return {
            'id': self.id,
            'address one': self.address_one,
            'city': self.city,
            'state': self.state,
            'zip code': self.zip_code
        }

# JOIN TABLES-------------------------------------------------

hymn_topic = db.Table(
    'hymn_topic', 
    db.Column('hymn_id', db.Integer, db.ForeignKey('hymn.id')),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'))
    )
    
# HYMN -------------------------------------------------

class Hymn(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    hymnal_number = db.Column(db.String(5), nullable = False)
    first_line = db.Column(db.String(100))
    title = db.Column(db.String(50), nullable = False)
    author = db.Column(db.String(50))
    meter = db.Column(db.String(50))
    language = db.Column(db.String(50))
    pub_date = db.Column(db.String(4))
    copyright = db.Column(db.String(200))
    tune_name = db.Column(db.String(20), nullable = False)
    arranger = db.Column(db.String(50))
    composer = db.Column(db.String(50))
    key = db.Column(db.String(5))
    source = db.Column(db.String(100))
    audio_rec = db.Column(db.String(200))
    choir_id = db.Column(db.Integer, db.ForeignKey('choir.id')) 
    tune_id = db.Column(db.Integer, db.ForeignKey('tune.id'))
    program = db.relationship('Program', backref = 'hymn')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Hymn {self.hymnal_number} | {self.title} >"

    def to_dict(self):
        return {
            'id': self.id,
            'Hymnal Number:': self.hymnal_number,
            'First Line:': self.first_line, 
            'Title:': self.title, 
            'Author:': self.author, 
            'Composer:': self.composer, 
            'Meter:': self.meter, 
            'Language:': self.language, 
            'Publication Date:': self.pub_date, 
            'Copyright:': self.copyright, 
            'Tune Name:': self.tune_name, 
            'Arranger:': self.arranger, 
            'Key:': self.key, 
            'Source:': self.source, 
            'Audio recording:' : self.audio_rec,
            'Topics:': [t.to_dict() for t in self.topics], 
            }

# TOPIC -------------------------------------------------

class Topic(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String(50), nullable = False)
    hymns = db.relationship('Hymn', secondary = hymn_topic, backref='topics')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Topic {self.id} | {self.topic} >"

    def to_dict(self):
        return {
            'id': self.id,
            'Topic:': self.topic, 
            }
    
# SERVICE ------------------------------------------------- 

class Service(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(10), nullable = False)
    program = db.relationship('Program', backref = 'service')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Service {self.id} | {self.date} >"

    def to_dict(self):
        return {
            'id': self.id,
            'Service Date:': self.date, 
            }

# TUNE -------------------------------------------------


class Tune(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    tune_name = db.Column(db.String(25), nullable = False)
    hymns = db.relationship('Hymn', backref = 'tune')
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Tune {self.id} | {self.tune_name} >"

    def to_dict(self):
        return {
            'id': self.id,
            'tune:': self.tune_name, 
            }
    
# PROGRAM -------------------------------------------------

class Program(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    hymn_id = db.Column(db.Integer, db.ForeignKey('hymn.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    conductor_id = db.Column(db.Integer, db.ForeignKey('conductor.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Program {self.id} | Service: {self.service_id} >"
    
    def to_dict(self):
        return  {
            'id': self.id,
            'hymn': self.hymn.to_dict(),
            'service': self.service.to_dict(), 
            }
    
