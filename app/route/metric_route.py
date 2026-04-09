from http import HTTPStatus
from flask import Blueprint, jsonify, request
from app.bll.services import metric_service
from app.schemas import MetricResponse
from app.utils.auth_handle import token_required

metric_bp = Blueprint('metric', __name__, url_prefix='/api/metrics')

@metric_bp.route('/<int:server_id>/metrics', methods=['GET'])
@token_required
def get_metrics(server_id: int):
    """
    Отримати історію метрик для конкретного сервера
    ---
    tags:
      - Server Metrics
    parameters:
      - in: path
        name: server_id
        type: integer
        required: true
        description: ID сервера, метрики якого потрібно отримати
      - in: query
        name: limit
        type: integer
        default: 20
        description: Кількість останніх записів для графіка
    responses:
      200:
        description: Список метрик у хронологічному порядку
        schema:
          type: array
          items:
            $ref: '#/definitions/MetricResponse'
      404:
        description: Сервер не знайдено
    """
    limit = request.args.get('limit', default=20, type=int)
    
    try:
        metrics = metric_service.get_server_history(server_id, limit)
        
        return jsonify([m.model_dump() for m in metrics]), HTTPStatus.OK
        
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"error": "Внутрішня помилка сервера"}), HTTPStatus.INTERNAL_SERVER_ERROR