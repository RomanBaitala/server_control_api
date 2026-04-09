from http import HTTPStatus
from flask import Blueprint, jsonify, request, make_response
from app.bll.services import user_service
from app.schemas import UserCreate, UserUpdate, UserLogin
from app.utils.auth_handle import generate_token, token_required

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/register', methods=['POST'])
def register():
    """
    Реєстрація нового користувача
    ---
    tags:
      - User API
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/UserCreate'
    responses:
      201:
        description: Користувача створено успішно
      400:
        description: Помилка валідації або такий Email вже існує
    """
    try:
        user_in = UserCreate(**request.get_json())
        new_user = user_service.register_user(user_in)
        return jsonify(new_user.model_dump()), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST


@user_bp.route('/login', methods=['POST'])
def login():
    """
    Авторизація користувача
    ---
    tags:
      - User API
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/UserLogin'
    responses:
      200:
        description: Успішний вхід
      401:
        description: Невірний email або пароль
    """
    try:
        login_in = UserLogin(**request.get_json())
        user = user_service.authenticate_user(login_in)
        
        if not user:
            return jsonify({"error": "Невірний email або пароль"}), HTTPStatus.UNAUTHORIZED
            
        token = generate_token(user.id)
        
        return jsonify({
            "message": "Вхід успішний",
            "token": token,
            "user": user.model_dump()
        }), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

@user_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_profile(user_id: int):
    """
    Отримати профіль користувача за ID
    ---
    tags:
      - User API
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: Дані профілю (без пароля)
      404:
        description: Користувача не знайдено
    """
    try:
        user = user_service.get_user_profile(user_id)
        return jsonify(user.model_dump()), HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND