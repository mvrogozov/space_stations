# Проект space stations.
***
Проект space stations служит для создания космических станций и их передвижения.
***

## Возможности.

* Добавление станции.
* Просмотр координат станции.
* При переходе в отрицательные координаты статус станции меняется на "broken".
***
***
После запуска через docker-compose необходимо создать БД (если еще нет) с именем указанным в переменной окружения DB_NAME
и настроить доступ к ней для пользователя указанного в переменной POSTGRES_USER:
```
docker exec -t -i yourdbcontainernumber bash
psql -U 'POSTGRES_USER'
CREATE DATABASE 'DB_NAME';
GRANT ALL PRIVILEGES ON DATABASE 'DB_NAME' TO 'POSTGRES_USER';
```
***
После этого необходимо выполнить миграции в контейнере backend:
```docker exec -t -i yourdbcontainernumber bash```
Перейти в папку с ```manage.py``` и выполнить 
```python3 manage.py migrate``` и ```python3 manage.py createsuperuser```

Переменные окружения, необходимые для запуска:

* DB_ENGINE - настройка ENGINE для БД в django.settings
* DB_HOST - имя хоста с БД (в проекте - 'db')
* DB_NAME - имя БД (в проекте - 'postgres')
* DB_PORT - порт для БД
* POSTGRES_PASSWORD - пароль БД
* POSTGRES_USER - пользователь БД
* DJANGO_SECRET_KEY - ключ для django проекта

Данные переменные необходимо сохранить в файле ```.env```в каталоге с manage.py
***
Потрачено времени около 13 часов.
***
Автор:
* Рогозов Михаил