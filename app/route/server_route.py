from http import HTTPStatus
from flask import Blueprint, jsonify, request, g
from app.bll.services import server_service
from app.schemas import ServerCreate, ServerUpdate
from app.utils.auth_handle import token_required

server_bp = Blueprint('server', __name__, url_prefix='/api/servers')

@server_bp.route('/', methods=['POST'])
@token_required
def add_server():
    """
    Додати новий сервер до облікового запису
    ---
    tags:
      - Server API
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            owner_id:
              type: integer
            name:
              type: string
              example: "Home-NAS"
            ip_address:
              type: string
              example: "192.168.1.10"
    responses:
      201:
        description: Сервер успішно додано
      400:
        description: Невірний формат даних або IP вже зайнятий
    """
    data = request.get_json()
    try:
        server_in = ServerCreate(**data)
        
        current_user_id = g.current_user_id
        
        new_server = server_service.create_server(current_user_id, server_in)
        return jsonify(new_server.model_dump()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@server_bp.route('/owner/<int:owner_id>', methods=['GET'])
@token_required
def list_servers(owner_id: int):
    """
    Отримати список усіх серверів власника
    ---
    tags:
      - Server API
    parameters:
      - in: path
        name: owner_id
        type: integer
        required: true
    responses:
      200:
        description: Список серверів користувача
        schema:
          type: array
          items:
            $ref: '#/definitions/ServerResponse'
    """
    servers = server_service.get_servers_by_owner(owner_id)
    return jsonify([s.model_dump() for s in servers]), HTTPStatus.OK

@server_bp.route('/<int:server_id>', methods=['PATCH'])
@token_required
def update_server(server_id: int):
    """
    Оновити дані сервера (назва, IP або статус)
    ---
    tags:
      - Server API
    parameters:
      - in: path
        name: server_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          $ref: '#/definitions/ServerUpdate'
    responses:
      200:
        description: Дані оновлено
      404:
        description: Сервер не знайдено
    """
    try:
        update_in = ServerUpdate(**request.get_json())
        updated = server_service.update_server(server_id, update_in)
        return jsonify(updated.model_dump()), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND