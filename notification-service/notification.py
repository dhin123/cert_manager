from flask import request, jsonify, Blueprint
from logs.logging_config import setup_logger

log = setup_logger(__file__)

noti_routes = Blueprint('noti_routes', __name__)


@noti_routes.route('/internal-notification', methods=['POST'])
def notification():
    from tasks import send_notification

    data = request.get_json()
    log.info(f"Received request to send notification with {data}")
    certificate_id = data["certificate_id"]
    status = data["status"]
    # dispatch the task
    task = send_notification.delay(certificate_id, status)
    return jsonify({
        "status": {
            "code": 200,
            "message": "Successfully notified external service",
            "task_id": str(task.id)

        }
    }), 200
    

