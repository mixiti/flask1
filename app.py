from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    score = db.Column(db.Integer, default=0)

# 在应用上下文中创建数据库表
def create_tables():
    with app.app_context():
        db.create_all()  # 创建所有数据库表

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    player_name = data.get('player_name')
    
    if player_name:
        player = Player.query.filter_by(name=player_name).first()
        if not player:
            player = Player(name=player_name)
            db.session.add(player)
            db.session.commit()
        
        return jsonify({"success": True, "message": "Game started!", "player_id": player.id}), 200
    return jsonify({"success": False, "message": "Player name is required!"}), 400

# 新增 API 路由：获取所有玩家的得分历史
@app.route('/get_scores', methods=['GET'])
def get_scores():
    players = Player.query.all()
    players_data = [{"name": player.name, "score": player.score} for player in players]
    return jsonify(players_data)

# 更新玩家得分
@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.get_json()
    player_id = data.get('player_id')
    score = data.get('score')

    if player_id is None or score is None:
        return jsonify({"success": False, "message": "Player ID and score are required!"}), 400
    
    player = Player.query.get(player_id)
    if player:
        player.score = score
        db.session.commit()
        return jsonify({"success": True, "message": "Score updated!"}), 200
    else:
        return jsonify({"success": False, "message": "Player not found!"}), 404

if __name__ == '__main__':
    create_tables()  # 在应用启动时创建数据库表
    app.run(debug=True)
