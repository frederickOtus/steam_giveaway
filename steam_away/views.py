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
        keys = Key.query.filter_by(owner_id=None)
        giveaways = Giveaway.query.all()
        return render_template('admin.html', 
                keys=keys, giveaways=giveaways, username=session['username'])
    else:
        return redirect(url_for('index'))

