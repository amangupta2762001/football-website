from flask import Blueprint, render_template, request, redirect, url_for
from .models import Team, Player
from . import db
from werkzeug.utils import secure_filename
import os
import time

bp = Blueprint('main', __name__)

def init_routes(app):
    app.register_blueprint(bp, url_prefix='/api')

@bp.route('/')
def index():
    players = Player.query.all()
    return render_template('index.html', players=players)

@bp.route('/teams')
def teams():
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)

@bp.route('/team/<int:id>')
def team(id):
    team = Team.query.get_or_404(id)
    return render_template('team.html', team=team)

@bp.route('/player/<int:id>')
def player(id):
    player = Player.query.get_or_404(id)
    return render_template('player.html', player=player)

@bp.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        if 'logo' in request.files:
            file = request.files['logo']
            if file.filename:
                filename = secure_filename(f"{name}_{int(time.time())}.png")
                file.save(os.path.join('app/static/uploads', filename))
                team = Team(name=name, country=country, logo=filename)
                db.session.add(team)
                db.session.commit()
        return redirect(url_for('main.teams'))
    return render_template('add_team.html')

@bp.route('/edit_team/<int:id>', methods=['GET', 'POST'])
def edit_team(id):
    team = Team.query.get_or_404(id)
    if request.method == 'POST':
        team.name = request.form['name']
        team.country = request.form['country']
        if 'logo' in request.files:
            file = request.files['logo']
            if file.filename:
                filename = secure_filename(f"{team.name}_{int(time.time())}.png")
                file.save(os.path.join('app/static/uploads', filename))
                team.logo = filename
        db.session.commit()
        return redirect(url_for('main.teams'))
    return render_template('edit_team.html', team=team)