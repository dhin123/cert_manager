import requests
from celery_config import app


@app.task(bind=True)
def send_notification(self, certificate_id, status):
    try:
        # send the notification to the external system
        external_system_url = "http://httpbin.org/post"
        response = requests.post(external_system_url, json={"message": "Certificate status has changed",
                                                            "certificate_id": certificate_id, "status": status})

        return response.text
    except Exception as e:
        raise self.retry(exc=e, countdown=60, max_retries=3)