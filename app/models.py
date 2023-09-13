import os
import base64
from app import db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password'))

    def __repr__(self):
        return f"< Conductor {self.id} | {self.username} >"
    
    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)
    
    def get_token(self, expires_in = 3600):
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
            'name': f'{self.first_name} {self.last_name}',
            'email': self.email,
            'username': self.username
        }

    @login.user_loader
    def load_user(user_id):
        return db.session.get(Conductor, user_id)
    
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
    
class Choir(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = False)
    hymns = db.relationship('Hymn', backref = 'choir', cascade = 'delete')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Address {self.id} | {self.address_one} >"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    
class Address(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    address_one = db.Column(db.String(100), nullable = False)
    address_two = db.Column(db.String(100))
    city = db.Column(db.String(30), nullable = False)
    zip_code = db.Column(db.String(10), nullable = False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Address {self.id} | {self.address_one} >"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
        }

hymn_topic = db.Table(
    'hymn_topic', 
    db.Column('hymn_id', db.Integer, db.ForeignKey('hymn.id')),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'))
    )

hymn_service_date = db.Table(
    'hymn_sunday', 
    db.Column('hymn_id', db.Integer, db.ForeignKey('hymn.id')),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'))
    )

class Hymn(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    hymnal_number = db.Column(db.String(5), nullable = False)
    first_line = db.Column(db.String(100), nullable = False)
    title = db.Column(db.String(50), nullable = False)
    author = db.Column(db.String(50), nullable = False)
    meter = db.Column(db.String(50), nullable = False)
    language = db.Column(db.String(50), nullable = False)
    pub_date = db.Column(db.String(4), nullable = False)
    copyright = db.Column(db.String(200))
    tune_name = db.Column(db.String(20), nullable = False)
    arranger = db.Column(db.String(50))
    key = db.Column(db.String(5))
    source = db.Column(db.String(100))
    audio_rec = db.Column(db.String(200))
    tune_id = db.Column(db.Integer, db.ForeignKey('tune.id'))
    service = db.relationship('Service', secondary = hymn_service_date, backref = 'hymns')

    # Foreign Key
    choir_id = db.Column(db.Integer, db.ForeignKey('choir.id')) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Hymn {self.id} | {self.title} >"

    def to_dict(self):
        return {
            'id': self.id,
            'Hymnal Number:': self.hymnal_number,
            'First Line:': self.first_line, 
            'Title:': self.title, 
            'Author:': self.author, 
            'Meter:': self.meter, 
            'Language:': self.language, 
            'Publication Date:': self.pub_date, 
            'Copyright:': self.copyright, 
            'Tune Name:': self.tune_name, 
            'Arranger:': self.arranger, 
            'Key:': self.key, 
            'Source:': self.source, 
            'Audio recording:' : self.audio_rec, 
            }

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

class Service(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(10), nullable = False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"< Service {self.id} | {self.date} >"

    def to_dict(self):
        return {
            'id': self.id,
            'Service Date:': self.date, 
            }

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