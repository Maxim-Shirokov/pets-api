# Pets rest api

Endpoints | Особенности
------------ | -------------
POST /pets | *name*: str(required) <br> *type*: str(required) <br> *age*: integer(optional, default=20)
POST /pets/{id}/photo | **form data** <br> file: binary
GET /pets |**query parameters:** <br> *limit*: integer(optional, default=0) <br> *offset*: integer(optional, default=20) <br> *has_photos*: boolean(optional)
DELETE /pets |**request body** <br> "ids": [list of ids]
### CLI
Выгрузка питомцев из командной строки в *stdout* в *JSON* формате

Необязательный параметр: *has_photos: boolean*

Пример: `python <PROJECT_PATH>/manage.py get --has_photos=True`
### Развертывание с помощью docker
Для развертывания используйте команду: `docker-compose -f <PROJECT_PATH>/docker-compose.yml up`

### Запуск тестов
Для запуска тестов используйте команду: `python <PROJECT_PATH>/manage.py test`

### Версии
*Python 3.9*

*Docker version 20.10.5*

*docker-compose version 1.29.0*
