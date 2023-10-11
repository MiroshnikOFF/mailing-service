Для корректной работы системы необходимо:
-----------------------------------------

- Установить все зависимости указанные в requirements.txt.
- Создать файл .env и внести в него все переменные окружения по образцу из файла .env.sample (по умолчанию в системе
  используется база данных PostgeSQL)
- Создать суперпользователя с помощью команды python manage.py ccsu.
- Запустить crontab с помощью команды python manage.py crontab add.
- В административной панели django создать группу user. Установить все разрешения для этой группы связанные с клиентами,
  сообщениями и рассылками, а также "Can view Лог" для просмотра отчета о проведенных рассылках.
- Установить и запустить redis.

Логика работы системы
---------------------
После создания новой рассылки, если текущее время больше времени начала и меньше времени окончания, выбираются из
справочника все клиенты, которые указаны в настройках рассылки, и запускается отправка
для всех этих клиентов. Если создается рассылка со временем старта в будущем, то отправка стартует автоматически по
наступлению этого времени без дополнительных действий со стороны пользователя системы.
По ходу отправки сообщений собирается статистика по каждой рассылке для последующего формирования отчетов.

Права доступа
-------------

- Для незарегистрированного пользователя открыт доступ только к главной странице и зарыт весь функционал системы
  за исключением страницы регистрации и страницы авторизации.
- Каждый зарегистрированный пользователь по умолчанию вносится в группу user.
- Каждый авторизованный пользователь имеет доступ только к своим клиентам, сообщениям, рассылкам и отчету о своих
  проведенных рассылках.
- Персонал может просматривать списки всех клиентов, сообщений, рассылок, пользователей сервиса и имеет доступ к отчету
  о всех проведенных рассылках.
- При наличии у пользователя разрешения "Can active mailing", он может включать и отключать рассылки.
- При наличии у персонала разрешения "Can active user", но может блокировать и активировать пользователей сервиса.