from datetime import datetime
from service.models import Mailing
from service.services import send_mailing


NOW_WITHOUT_SECONDS = datetime.now().time().replace(second=0, microsecond=0)


def send_message() -> None:
    """
    Получает из БД все рассылки предназначенные для отправки и если текущая дата совпадает с датой в поле next_run,
    то запускает рассылки по времени указанном в поле start. Cron-функция срабатывает каждую минуту.
    """
    mailings = Mailing.objects.filter(status='Создана').filter(next_run=datetime.now().date())
    for mailing in mailings:
        if mailing.start == NOW_WITHOUT_SECONDS:
            send_mailing(mailing.pk)
