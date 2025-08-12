from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Player, Team
from werkzeug.utils import secure_filename
import os
import time

def init_routes(app):
    # Use normalized absolute path for UPLOAD_FOLDER
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.normpath(os.path.join(base_dir, 'static', 'uploads'))
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @app.route('/')
    def index():
        # Add sample data (only runs if database is empty)
        if Team.query.count() == 0:
            team1 = Team(name='Manchester United', country='England')
            team2 = Team(name='Real Madrid', country='Spain')
            db.session.add_all([team1, team2])
            db.session.commit()
            
            player1 = Player(name='Marcus Rashford', position='Forward', market_value=70000000, team_id=team1.id, goals=10, assists=5, matches_played=30)
            player2 = Player(name='Vinicius Jr', position='Forward', market_value=150000000, team_id=team2.id, goals=15, assists=8, matches_played=28)
            db.session.add_all([player1, player2])
            db.session.commit()
        
        # Handle sorting
        sort_by = request.args.get('sort_by', 'name')
        sort_order = request.args.get('sort_order', 'asc')
        
        players_query = Player.query.join(Team)
        if sort_by == 'name':
            players_query = players_query.order_by(Player.name.asc() if sort_order == 'asc' else Player.name.desc())
        elif sort_by == 'market_value':
            players_query = players_query.order_by(Player.market_value.asc() if sort_order == 'asc' else Player.market_value.desc())
        elif sort_by == 'goals':
            players_query = players_query.order_by(Player.goals.asc() if sort_order == 'asc' else Player.goals.desc())
        
        players = players_query.all()
        teams = Team.query.all()
        return render_template('index.html', players=players, teams=teams, sort_by=sort_by, sort_order=sort_order)
    
    @app.route('/add_player', methods=['GET', 'POST'])
    def add_player():
        if request.method == 'POST':
            name = request.form['name']
            position = request.form['position']
            market_value = int(request.form['market_value'])
            team_id = int(request.form['team_id'])
            goals = int(request.form['goals'])
            assists = int(request.form['assists'])
            matches_played = int(request.form['matches_played'])
            player = Player(name=name, position=position, market_value=market_value, team_id=team_id, goals=goals, assists=assists, matches_played=matches_played)
            db.session.add(player)
            db.session.commit()
            flash('Player added successfully!', 'success')
            return redirect(url_for('index'))
        
        teams = Team.query.all()
        return render_template('add_player.html', teams=teams)
    
    @app.route('/edit_player/<int:id>', methods=['GET', 'POST'])
    def edit_player(id):
        player = Player.query.get_or_404(id)
        if request.method == 'POST':
            player.name = request.form['name']
            player.position = request.form['position']
            player.market_value = int(request.form['market_value'])
            player.team_id = int(request.form['team_id'])
            player.goals = int(request.form['goals'])
            player.assists = int(request.form['assists'])
            player.matches_played = int(request.form['matches_played'])
            db.session.commit()
            flash('Player updated successfully!', 'success')
            return redirect(url_for('index'))
        
        teams = Team.query.all()
        return render_template('edit_player.html', player=player, teams=teams)
    
    @app.route('/delete_player/<int:id>')
    def delete_player(id):
        player = Player.query.get_or_404(id)
        db.session.delete(player)
        db.session.commit()
        flash('Player deleted successfully!', 'success')
        return redirect(url_for('index'))
    
    @app.route('/teams')
    def teams():
        teams = Team.query.all()
        return render_template('teams.html', teams=teams)
    
    @app.route('/add_team', methods=['GET', 'POST'])
    def add_team():
        if request.method == 'POST':
            name = request.form['name']
            country = request.form['country']
            team = Team(name=name, country=country)
            db.session.add(team)
            db.session.commit()
            
            if 'logo' in request.files:
                file = request.files['logo']
                print(f"File received: {file.filename}")
                if file and allowed_file(file.filename):
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = f"{name.lower().replace(' ', '_')}_{int(time.time())}.{ext}"
                    filename = secure_filename(filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    print(f"UPLOAD_FOLDER: {app.config['UPLOAD_FOLDER']}")
                    print(f"Saving file: {filename} to {file_path}")
                    try:
                        # Ensure uploads directory exists
                        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                        file.save(file_path)
                        team.logo = filename
                        db.session.commit()
                        print(f"Logo saved in DB: {team.logo}")
                        flash('Team added successfully!', 'success')
                    except Exception as e:
                        print(f"Error saving file: {str(e)}")
                        flash(f'Failed to upload logo: {str(e)}', 'error')
                else:
                    print("Invalid file or no file uploaded")
                    flash('Invalid file format. Use PNG, JPG, JPEG, GIF, or WEBP.', 'error')
            
            return redirect(url_for('teams'))
        
        return render_template('add_team.html')
    
    @app.route('/edit_team/<int:id>', methods=['GET', 'POST'])
    def edit_team(id):
        team = Team.query.get_or_404(id)
        if request.method == 'POST':
            team.name = request.form['name']
            team.country = request.form['country']
            
            if 'logo' in request.files:
                file = request.files['logo']
                print(f"File received: {file.filename}")
                if file and allowed_file(file.filename):
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = f"{team.name.lower().replace(' ', '_')}_{int(time.time())}.{ext}"
                    filename = secure_filename(filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    print(f"UPLOAD_FOLDER: {app.config['UPLOAD_FOLDER']}")
                    print(f"Saving file: {filename} to {file_path}")
                    try:
                        # Ensure uploads directory exists
                        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                        file.save(file_path)
                        team.logo = filename
                        print(f"Logo saved in DB: {team.logo}")
                        flash('Team updated successfully!', 'success')
                    except Exception as e:
                        print(f"Error saving file: {str(e)}")
                        flash(f'Failed to upload logo: {str(e)}', 'error')
                else:
                    print("Invalid file or no file uploaded")
                    flash('Invalid file format. Use PNG, JPG, JPEG, GIF, or WEBP.', 'error')
            
            db.session.commit()
            return redirect(url_for('teams'))
        
        return render_template('edit_team.html', team=team)
    
    @app.route('/delete_team/<int:id>')
    def delete_team(id):
        team = Team.query.get_or_404(id)
        if Player.query.filter_by(team_id=id).count() > 0:
            flash('Cannot delete team with associated players.', 'error')
            return render_template('teams.html', teams=Team.query.all())
        db.session.delete(team)
        db.session.commit()
        flash('Team deleted successfully!', 'success')
        return redirect(url_for('teams'))
    
    @app.route('/search', methods=['GET', 'POST'])
    def search():
        if request.method == 'POST':
            query = request.form['query']
            players = Player.query.join(Team).filter(
                (Player.name.ilike(f'%{query}%')) | 
                (Team.name.ilike(f'%{query}%')) | 
                (Player.position.ilike(f'%{query}%'))
            ).all()
            teams = Team.query.all()
            return render_template('index.html', players=players, teams=teams, query=query)
        return redirect(url_for('index'))
    
    @app.route('/player/<int:id>')
    def player_details(id):
        player = Player.query.get_or_404(id)
        return render_template('player_details.html', player=player)
    
    @app.route('/team/<int:id>')
    def team_details(id):
        team = Team.query.get_or_404(id)
        players = Player.query.filter_by(team_id=id).all()
        return render_template('team_details.html', team=team, players=players)