from datetime import datetime, timedelta
from fastapi import UploadFile
from redis import Redis
from rq import Queue

from ai_health.root.settings import Settings

settings = Settings()

queue = Queue(connection=Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT))


# def background_mailer(
#     reciepients: list[str],
#     subject: str,
#     payload: dict,
#     template: str,
#     attachments: list[UploadFile] = [],
# ):
#     job = queue.enqueue_at(
#         datetime=datetime.now(),
#         # time_delta=timedelta(seconds=1),
#         f=send_mail,
#         subject=subject,
#         reciepients=reciepients,
#         payload=payload,
#         template=template,
#         attachments=attachments,
#     )


    # print(f"This is the job result {job.result}")
