# Учебный журнал · Learning Log

Личный журнал по проекту учебника [Python & Django](https://xn--80aaxhb0ahs.xn--h1adrf.xn--p1ai/proekt-learning_log.html). После регистрации пользователь может создавать темы, добавлять к ним заметки и редактировать записи. Django проверяет владельца темы при просмотре и изменениях. Интерфейс на русском языке использует Bootstrap 4.

## Адреса для сдачи

- [Публичный репозиторий GitHub](https://github.com/VLAADOS1/learning-log)
- [Приложение по HTTPS](https://learning-log.201-3-225-35.sslip.io/)
- [IP и порт сервера Pixta](http://201.3.225.35:20010/) перенаправляют на HTTPS.

## Развёртывание на учебном сервере

Понадобятся Docker и Docker Compose. Склонируйте проект и создайте файл настроек.

```sh
git clone https://github.com/VLAADOS1/learning-log.git
cd learning-log
cp .env.example .env
openssl rand -hex 48
```

Сохраните сгенерированное значение в `DJANGO_SECRET_KEY`. Укажите IP учебного сервера в `DJANGO_ALLOWED_HOSTS`, а выделенный порт в `APP_PORT`. Запустите:

```sh
docker compose up -d --build
docker compose ps
docker compose logs --tail=50 web
```

Откройте `http://IP:ПОРТ/` и зарегистрируйтесь. При старте контейнер применяет миграции и собирает статические файлы. SQLite хранится в томе `journal_data`. Пересоздание контейнера сохраняет записи. Для доступа к Django Admin создайте суперпользователя командой `docker compose exec web python manage.py createsuperuser` и откройте `/admin/`.

## Настройки окружения

| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | Случайный секрет Django. При выключенной отладке обязателен. |
| `DJANGO_DEBUG` | Оставьте `False` на сервере. |
| `DJANGO_ALLOWED_HOSTS` | IP и домены через запятую, без схемы и порта. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | При необходимости доверенные источники через запятую, со схемой и нестандартным портом. |
| `DJANGO_USE_HTTPS` | `True` за доверенным HTTPS-прокси. Включает защищённые cookies и перенаправление на HTTPS. |
| `APP_BIND_IP`, `APP_PORT` | Внешний адрес и порт Docker. В примере `0.0.0.0` и `20010`. |
| `APP_HOST` | Домен журнала для конфигурации Traefik. |
| `SQLITE_PATH` | Путь к SQLite. В Compose задан как `/app/data/db.sqlite3`. |

## Деплой по HTTPS на Pixta

Конфигурация использует существующий Traefik с сетью `traefik_proxy`, точкой входа `websecure` и ACME-резолвером `le`. Укажите домен в `APP_HOST` и `DJANGO_ALLOWED_HOSTS`, полный HTTPS-адрес в `DJANGO_CSRF_TRUSTED_ORIGINS` и установите `DJANGO_USE_HTTPS=True`. На Pixta выбран домен `learning-log.201-3-225-35.sslip.io`, который разрешается в IP сервера.

```sh
docker compose -f compose.yaml -f compose.traefik.yaml -f compose.ip-redirect.yaml up -d --build
```

Приложение получает трафик из сети Traefik. Дополнительный контейнер на порту `20010` перенаправляет браузер с IP-адреса на HTTPS-домен.

## Локальный запуск

Создайте окружение Python 3.12 командой `python3.12 -m venv .venv` или `py -3.12 -m venv .venv` в Windows. Активируйте его командой `source .venv/bin/activate` или `.\.venv\Scripts\Activate.ps1` в PowerShell, затем выполните:

```sh
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py test
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`. Тесты проверяют вход и выход, создание темы, создание и редактирование записи, а также запрет доступа к чужим данным.
