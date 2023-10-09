from datetime import datetime
from service.models import Mailing
from service.services import send


NOW_WITHOUT_SECONDS = datetime.now().time().replace(second=0, microsecond=0)


def send_message():
    mailings = Mailing.objects.filter(status='Создана').filter(next_run=datetime.now().date())
    for mailing in mailings:
        if mailing.start == NOW_WITHOUT_SECONDS:
            send(mailing.pk)
