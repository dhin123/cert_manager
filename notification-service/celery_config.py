from celery import Celery


app = Celery('tasks', broker='pyamqp://guest:guest@rabbitmq:5672/', result_persistent=True)
app.conf.update(
    # Configure the result backend using MySQL
    CELERY_RESULT_BACKEND='db+mysql+pymysql://root:my-secret-pw@mysql:3306/mydatabase',

    CELERY_TASK_SERIALIZER='json',

    # Do not ignore results (set to False)
    CELERY_IGNORE_RESULT=False,


)
app.conf.CELERY_ACCEPT_CONTENT = ["json", "msgpack"]

app.conf.CELERY_RESULT_SERIALIZER = "msgpack"