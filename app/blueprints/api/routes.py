from . import api
from app import db
from app.models import Address, Conductor, Organization, Choir, Hymn, Program, Service, Topic, Tune
from flask import request
from .auth import basic_auth, token_auth
from bs4 import BeautifulSoup
import requests

# GET USER TOKEN --------------------------------

@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user = basic_auth.current_user()
    token = auth_user.get_token()
    return {'token': token,
            'token_exp': auth_user.token_expiration}

# GET USER = ME --------------------------------------------------

@api.route('/users/me')
@token_auth.login_required
def get_me():
    me = token_auth.current_user()
    return me.to_dict()

# CREATE USER --------------------------------------------------

@api.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return{'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        if missing_fields:
            return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
        
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    check_user = db.session.execute(db.select(Conductor).where((Conductor.username == username) | (Conductor.email == email))).scalar()

    if check_user:
        {'error': f'A user with that username and/or email already exists'}, 400

    new_user = Conductor(first_name = first_name, last_name = last_name, email = email, username = username,  password = password)

    db.session.add(new_user)
    db.session.commit()

    return new_user.to_dict(),201

# LOGIN USER --------------------------------------------------

@api.route('/login', methods=["GET"])
@basic_auth.login_required
def login_user():
    logged_in_user = basic_auth.current_user()
    return logged_in_user.to_dict(),201

# EDIT USER --------------------------------------------------

@api.route('/users', methods=["PUT"])
@token_auth.login_required
def edit_user():
    auth_user = token_auth.current_user()
    data = request.json
    print('//////////', data)
    for field in data:
        if field in {'firstName', 'lastName', 'username', 'email'}:
            if field == 'firstName':
                setattr(auth_user, 'first_name', data[field])
            elif field == 'lastName':
                setattr(auth_user, 'last_name', data[field])
            else:
                setattr(auth_user, field, data[field])
    db.session.commit()
    return auth_user.to_dict(),201

# DELETE USER --------------------------------------------------

@api.route('/users', methods=["DELETE"])
@token_auth.login_required
def delete_user():
    auth_user = token_auth.current_user()
    db.session.delete(auth_user)
    db.session.commit()
    return {'success': f"{auth_user.first_name} has been deleted"}, 201


# GET USER PROGRAMS --------------------------------------------------

@api.route('/users/programs')
@token_auth.login_required
def get_user_programs():
    current_user = token_auth.current_user()
    programs = [p.to_dict() for p in current_user.programs]
    programs_li=[]
    for p in programs:
        programs_li.append({ 'key': f"{p['id']}", 'service': f"{p['service']['Service Date:']}", 'hymnalnum': f"{p['hymn']['Hymnal Number:']}", 'title': f"{p['hymn']['Title:']}", 'tune': f"{p['hymn']['Tune Name:']}", 'key_mus': f"{p['hymn']['Key:']}", 'topics': [f"{t['Topic:']} / " for t in p['hymn']['Topics:']]})

    return programs_li

# CREATE ADDRESS --------------------------------------------------

@api.route('/address', methods=['POST'])
def create_address():
    if not request.is_json:
        return{'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['addressOne', 'city', 'state', 'zipCode']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        if missing_fields:
            return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
        
    address_one = data.get('addressOne')
    address_two = data.get('addressTwo')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zipCode')

    check_user = db.session.execute(db.select(Address).where((Address.address_one == address_one))).scalar()

    if check_user:
        {'error': f'A user with that username and/or email already exists'}, 400

    new_address = Address(address_one = address_one, address_two = address_two, city = city, state = state, zip_code = zip_code)

    db.session.add(new_address)
    db.session.commit()

    return new_address.to_dict(),201


# EDIT ADDRESS ---------------------------------------------------------

# How should I select the address that belongs to this user's organization? An Organization ID FK on address?


# CREATE ORGANIZATION --------------------------------------------------

@api.route('/orgs', methods=['POST'])
@token_auth.login_required
def create_organization():
    if not request.is_json:
        return{'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['name', 'email', 'website']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        if missing_fields:
            return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
        
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    website = data.get('website')
    current_user = token_auth.current_user()

    check_org = db.session.execute(db.select(Organization).where((Organization.name == name))).scalar()
    if check_org:
        {'error': f'A user with that username and/or email already exists'}, 400

    new_org = Organization(name = name, phone = phone, email = email, website = website, conductor_id = current_user.id)

    db.session.add(new_org)
    db.session.commit()

    return new_org.to_dict(),201

# EDIT ORGANIZATION --------------------------------------------------

@api.route('/orgs/<org_id>', methods=['PUT'])
@token_auth.login_required
def edit_organization(org_id):
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    
    org = db.session.get(Organization, org_id)

    if org is None:
        return {'error': f'Organization with an ID of {org_id} does not exist'}, 404
    current_user = token_auth.current_user()
    
    if org.conductor_id != current_user.id:
            return {'error': 'You do not have permission to edit this organization.'}, 403

    data = request.json
    for field in data:
        if field in {'name', 'email', 'phone', 'website'}:
            setattr(org, field, data[field])
    db.session.commit()
    return org.to_dict()

# DELETE ORGANIZATION --------------------------------------------------

@api.route('/orgs/<org_id>', methods=['DELETE'])
@token_auth.login_required
def delete_organization(org_id):    
    org = db.session.get(Organization, org_id)

    if org_id is None:
        return {'error': f'Organization with an ID of {org_id} does not exist'}, 404
    current_user = token_auth.current_user()

    if org.conductor_id != current_user.id:
        return {'error': f'User with user id {current_user.id} do not have permission to delete this organization'}, 403

    db.session.delete(org)
    db.session.commit()
    return {'success': f"{org.name} has been deleted"}

# CREATE CHOIR --------------------------------

@api.route('/choirs', methods=['POST'])
@token_auth.login_required
def create_choir():
    if not request.is_json:
        return{'error': 'Your content-type must be application/json'}, 400
    data = request.json

    name = data.get('choirName')
    current_user = token_auth.current_user()
    current_organization = db.session.execute(db.select(Organization).where(Organization.conductor_id == current_user.id)).scalar()
    
    check_choir = db.session.execute(db.select(Choir).where((Choir.name == name))).scalar()

    if check_choir:
        return {'error': f'A choir with that name already exists in your organization'}, 400

    new_choir = Choir(name = name, organization_id = current_organization.id)

    db.session.add(new_choir)
    db.session.commit()

    return new_choir.to_dict(),201

# EDIT CHOIR --------------------------------

@api.route('/choirs/<choir_id>', methods=['PUT'])
@token_auth.login_required
def edit_choir(choir_id):
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    
    choir = db.session.get(Choir, choir_id)

    if choir is None:
        return {'error': f'Organization with an ID of {choir_id} does not exist'}, 404
    current_user = token_auth.current_user()

    if choir.conductor_id != current_user:
            return {'error': 'You do not have permission to edit this choir.'}, 403

    data = request.json

    if 'name' in data:
        setattr(choir, 'name', data['name'])

    db.session.commit()
    return choir.to_dict(), 201

# DELETE CHOIR --------------------------------

@api.route('/choirs/<choir_id>', methods=['DELETE'])
@token_auth.login_required
def delete_choir(choir_id):    
    choir = db.session.get(Choir, choir_id)

    if choir_id is None:
        return {'error': f'Organization with an ID of {choir_id} does not exist'}, 404
    current_user = token_auth.current_user()

    if choir.conductor_id != current_user.id:
        return {'error': f'User with user id {current_user.id} do not have permission to delete this choir'}, 403

    db.session.delete(choir)
    db.session.commit()
    return {'success': f"{choir.name} has been deleted"}


# CREATE HYMN --------------------------------

@api.route('/hymns', methods=['POST'])
@token_auth.login_required
def create_hymn():
    if not request.is_json:
        return{'error': 'Your content-type must be application/json'}, 400
    current_user = token_auth.current_user()
    
    data = request.json

    required_fields = ["first_line", "title", "author", "meter", "language", "pub_date", "copyright", "tune_name"]
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        if missing_fields:
            return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400

    id = data.get('id')
    first_line = data.get('first_line')
    title = data.get('title')
    author = data.get('author')
    meter = data.get('meter')
    language = data.get('language')
    pub_date = data.get('pub_date')
    copyright = data.get('copyright')
    tune_name = data.get('tune_name')
    arranger = data.get('arranger')
    key = data.get('key')
    source = data.get('source')
    audio_rec = data.get('audio_rec')
    choir_id =  data.get('choir_id')
    
    check_hymn = db.session.execute(db.select(Hymn).where((Hymn.title == title))).scalar()

    if check_hymn:
        return {'error': f'A hymn with that title already'}, 400

    new_hymn = Hymn(id = id, first_line = first_line, title = title, author = author, meter = meter, language = language, pub_date = pub_date, copyright = copyright, tune_name = tune_name, arranger = arranger, key = key, source = source, audio_rec = audio_rec, choir_id = choir_id,)

    db.session.add(new_hymn)
    db.session.commit()

    return new_hymn.to_dict(),201

# CREATE WEB SCRAPE HYMN --------------------------------

@api.route('/hymns/<hymn_id>', methods=['POST'])
@token_auth.login_required
def find_hymn(hymn_id):

    check_db_hymn = db.session.execute(db.select(Hymn).where((Hymn.hymnal_number == hymn_id))).scalar()
    if check_db_hymn:
        return check_db_hymn.to_dict(),201

    url = f'https://hymnary.org/hymn/GG2013/{hymn_id}'
    result = requests.get(url).text
    doc = BeautifulSoup(result, 'html.parser')

    trs = doc.find_all(class_='result-row')

    info = {}
    scriptures = []
    for tr in trs:
        for td in [tr.contents]:
            key_name = td[0].span.string
            if td[2].span.string:
                info[key_name] = td[2].span.string
            elif key_name == 'Scripture:':
                for i in range(len(td[2].span.contents)):
                    scripture_values = td[2].span.contents[i].string
                    if '; ' in scripture_values:
                        pass
                    else:
                        scriptures.append(scripture_values)
                        info[key_name] = scriptures
            elif key_name == 'Topic:':
                info[key_name] = f'{td[2].span.contents[0].string}{td[2].span.span.string}'.split('; ')
            elif key_name == 'Audio recording:':
                info[key_name] = td[2].a.get('href')
            elif key_name == 'Composer:':
                info[key_name] = td[2].span.a.string
            elif key_name == 'Source:':
                info[key_name] = td[2].span.contents[0].string
            else:
                info[key_name] = td[2].a.string

    if info == {}:
        return {'error': f'Hymn with hymn id {hymn_id} does not exist'}, 403

    current_user = token_auth.current_user()
    current_organization = db.session.execute(db.select(Organization).where(Organization.conductor_id == current_user.id)).scalar()
    current_choir = db.session.execute(db.select(Choir).where(Choir.organization_id == current_organization.id)).scalar()

    hymnal_number = hymn_id
    first_line = info.get('First Line:')
    title = info.get('Title:')
    author = info.get('Author:')
    meter = info.get('Meter:')
    language = info.get('Language:')
    pub_date = info.get('Publication Date:')
    copyright = info.get('Copyright:')
    tune_name = info.get('Name:')
    arranger = info.get('Arranger:')
    composer = info.get('Composer:')
    key = info.get('Key:')
    source = info.get('Source:')
    audio_rec = info.get('Audio recording:')
    choir_id =  current_choir.id
    
    new_tune = Tune(tune_name=tune_name)
    db.session.add(new_tune)
    db.session.commit()

    selected_tune = db.session.execute(db.select(Tune).where(Tune.tune_name == info.get('Name:'))).scalar()

    new_hymn = Hymn(hymnal_number = hymnal_number, first_line = first_line, title = title, author = author, meter = meter, language = language, pub_date = pub_date, copyright = copyright, tune_name = tune_name, arranger = arranger, composer = composer, key = key, source = source, audio_rec = audio_rec, choir_id = choir_id, tune_id = selected_tune.id)

    db.session.add(new_hymn)

    # Create Relationship for hymn_topic table
    for topic in info.get('Topic:'):
        selected_topic = db.session.execute(db.select(Topic).where((Topic.topic == topic))).scalar()
        if selected_topic:
            new_hymn.topics.append(selected_topic)

    db.session.commit()

    return new_hymn.to_dict(),201

# # DISPLAY HYMN --------------------------------

@api.route('/hymns/display/<hymn_id>', methods=['GET'])
@token_auth.login_required
def display_hymn(hymn_id):

    hymn_to_display = db.session.execute(db.select(Hymn).where(Hymn.hymnal_number == hymn_id)).scalar()

    if not hymn_to_display:
        return {'error:': 'Hymn not in your database'}

    hymn_to_return = [
        { 'key': '1', 'label': 'Title', 'children': f'{hymn_to_display.title}', }, 
        { 'key': '2', 'label': 'Number', 'children': f'{hymn_to_display.hymnal_number}', }, 
        { 'key': '3', 'label': 'Tune', 'children': f'{hymn_to_display.tune_name}', }, 
        { 'key': '4', 'label': 'Key', 'children': f'{hymn_to_display.key}', }, 
        { 'key': '5', 'label': 'Last Programmed', 'span': 2, 'children': '2019-04-24', }, 
        { 'key': '6', 'label': 'Author', 'children': 'John Ernest Bode', }, 
        { 'key': '7', 'label': 'Meter', 'children': f'{hymn_to_display.meter}', }, 
        { 'key': '8', 'label': 'Language', 'children': f'{hymn_to_display.language}', }, 
        { 'key': '9', 'label': 'Copyright', 'children': f'{hymn_to_display.copyright}' }]
    
    return hymn_to_return, 201

# # PROGRAM HYMNS --------------------------------

# @api.route('/program/<service_id>/<hymn_number>', methods=['POST'])
# @token_auth.login_required
# def program_hymn(service_id, hymn_number):
#     current_user = token_auth.current_user()
    
#     selected_service = db.session.execute(db.select(Service).where((Service.id == service_id))).scalar()
#     selected_hymn = db.session.execute(db.select(Hymn).where(Hymn.hymnal_number == hymn_number)).scalar()

#     if selected_service is None:
#         return {'error': f'Service with an id of {service_id} does not exist'}, 400
#     if selected_hymn is None:
#         return {'error': f'Hymn with an id of {hymn_number} does not exist'}, 400
    
#     conductor_id = current_user.id
#     hymn_id_number = selected_hymn.id
#     service_id_number = selected_service.id

#     new_program = Program(conductor_id = conductor_id, hymn_id = hymn_id_number, service_id = service_id_number)
#     db.session.add(new_program)
#     db.session.commit()

#     return selected_service.to_dict(),201

# PROGRAM HYMNS --------------------------------

@api.route('/program/<service_date>/<hymn_number>', methods=['POST'])
@token_auth.login_required
def program_hymn_by_date(service_date, hymn_number):
    current_user = token_auth.current_user()
    
    selected_service = db.session.execute(db.select(Service).where((Service.date == service_date))).scalar()
    selected_hymn = db.session.execute(db.select(Hymn).where(Hymn.hymnal_number == hymn_number)).scalar()

    if selected_service is None:
        return {'error': f'Service with a date of {service_date} does not exist'}, 400
    if selected_hymn is None:
        return {'error': f'Hymn with an id of {hymn_number} does not exist'}, 400
    
    conductor_id = current_user.id
    hymn_id_number = selected_hymn.id
    service_id_number = selected_service.id

    new_program = Program(conductor_id = conductor_id, hymn_id = hymn_id_number, service_id = service_id_number)
    db.session.add(new_program)
    db.session.commit()

    return selected_service.to_dict(),201

# EDIT PROGRAM HYMNS --------------------------------

@api.route('program/<service_date>/<hymn_number>', methods=['DELETE'])
@token_auth.login_required
def delete_hymn_from_service(service_date, hymn_number):

    current_user = token_auth.current_user()
    # print('current user id:', current_user.id)
    selected_service = db.session.execute(db.select(Service).where((Service.date == service_date))).scalar()
    # print('selected service date:', selected_service.id)
    selected_hymn = db.session.execute(db.select(Hymn).where(Hymn.hymnal_number == hymn_number)).scalar()
    # print('selected hymn number:', selected_hymn.id)
    program_to_delete = db.session.execute(db.select(Program).where((Program.service_id == selected_service.id) & (Program.hymn_id == selected_hymn.id) & (Program.conductor_id == current_user.id))).scalar()
    # print('program to delete:', program_to_delete)

    if program_to_delete is None:
        return {'error': f'Program does not exist'}, 404
    
    print('program to delete conductor id',  program_to_delete.conductor_id)

    if program_to_delete.conductor_id != current_user.id:
        return {'error': f'User with user id {current_user.id} do not have permission to edit this program'}, 403

    db.session.delete(program_to_delete)
    db.session.commit()
    return {'success': f"{program_to_delete.id} has been deleted"}