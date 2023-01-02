from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Player, player_schema, players_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/players', methods = ['POST'])
@token_required
def create_player(current_user_token):
    name = request.json['name']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    player = Player(name, user_token = user_token )

    db.session.add(player)
    db.session.commit()

    response = player_schema.dump(player)
    return jsonify(response)

@api.route('/players', methods = ['GET'])
@token_required
def get_player(current_user_token):
    a_user = current_user_token.token
    players = Player.query.filter_by(user_token = a_user).all()
    response = players_schema.dump(players)
    return jsonify(response)

@api.route('/players/<id>', methods = ['POST','PUT'])
@token_required
def update_player(current_user_token,id):
    player = Player.query.get(id) 
    player.user_token = current_user_token.token

    db.session.commit()
    response = player_schema.dump(player)
    return jsonify(response)

@api.route('/players/<id>', methods = ['DELETE'])
@token_required
def delete_player(current_user_token, id):
    player = Player.query.get(id)
    db.session.delete(player)
    db.session.commit()
    response = player_schema.dump(player)
    return jsonify(response)