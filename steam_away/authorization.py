from steam_away import app, db
from steam_away.models import Person
from flask import session, request, url_for, redirect
from apiclient.discovery import build
from oauth2client import client

import httplib2
import json

@app.before_request
def enforce_login():
    if not request.endpoint in ['login','logout']:
        if not session.get('credentials'):
            return redirect(url_for('login'))
        credentials = client.OAuth2Credentials.from_json(session['credentials'])
        
        if credentials.access_token_expired:
            return redirect(url_for('login'))
        

        if 'username' not in session:
            http_auth = credentials.authorize(httplib2.Http())
            service = build('plus','v1', http_auth)
            peeps = service.people()
            profile = peeps.get(userId='me').execute()
            uid = profile['id']
            userq = Person.query.filter_by(oauth_id=uid)
            if(userq.count() == 0):
                print('new user!')
                user = Person(profile['displayName'], uid)
                db.session.add(user)
                db.session.commit()
            else:
                print('user found!')
                user = userq.first()

            session['uid'] = user.id
            session['username'] = profile['displayName']
            session['admin'] = user.admin

@app.route('/login')
def login():
    flow = client.flow_from_clientsecrets(
        'steam_away/client_secret.json',
        scope='https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
        redirect_uri='http://localhost:5000/login',
    )

    err = request.args.get('error')
    code = request.args.get('code')
    if err:
        return err
    elif code:
        credentials = flow.step2_exchange(code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('index'))
    else:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    
@app.route('/logout')
def logout():
    session.clear()
    return "BAI!"
