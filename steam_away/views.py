from flask import *
from steam_away.models import *
from steam_away import app

@app.route('/')
def index():
    giveaway = Giveaway.query.filter_by(active=True).first()
    return render_template('index.html', username=session['username'], giveaway=giveaway)

@app.route('/admin')
def admin():
    if session['admin']:
        keys = Key.query.filter_by(giveaway_id=None)
        giveaways = Giveaway.query.filter_by(active=False)
        return render_template('admin.html', 
                keys=keys, giveaways=giveaways, username=session['username'])
    else:
        return redirect(url_for('index'))

# ajax routes
@app.route('/key/add/<name>/<key>')
def add_key(name, key):
    if len(name) == 0 or len(key) == 0:
        return json.dumps({"error": "cant have empty vals"}), 400
    if Key.query.filter_by(key=key).count() == 0:
        k = Key(name, key)
        db.session.add(k)
        db.session.commit()
        return json.dumps({"id":k.id})
    else:
        return json.dumps({"error":"key already exists"}), 400


@app.route('/key/set_giveaway/<key_id>/<ga_id>')
def set_key_giveaway(key_id, ga_id):
    key = Key.query.filter_by(id=key_id).first_or_404()
    if int(ga_id) == 0:
        giveaway = None
    else:
        giveaway = Giveaway.query.filter_by(id=ga_id).first_or_404()
    key.giveaway = giveaway
    db.session.commit()
    return ""

@app.route('/giveaway/add/<name>')
def add_giveaway(name):
    if len(name) == 0:
        return json.dumps({'error':'cant have empty name'}),400
    ga = Giveaway(name)
    db.session.add(ga)
    db.session.commit()
    return json.dumps({'id':ga.id})

@app.route('/giveaway/activate/<ga_id>')
def activate_giveaway(ga_id):
    g = Giveaway.query.filter_by(id=ga_id).first_or_404()
    gas = Giveaway.query.filter_by(active=True)
    for ga in gas:
        ga.active = False
    g.active=True
    db.session.commit()
    return ""

@app.route('/giveaway/deactivate')
def deactivate_giveaway(ga_id):
    ga = Giveaway.query.filter_by(active=True).first()
    if not ga is None:
        ga.active = True
        db.session.commit()
    return ""
