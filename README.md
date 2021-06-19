# Pets rest api

Endpoints | Особенности
------------ | -------------
POST /pets | name: str(required) <br> type: str(required) <br> age: integer(optional, default=20)
POST /pets/{id}/photo | `form data` <br> file: binary
GET /pets |`query parameters:` <br> limit: integer(optional, default=20) <br> offset: integer(optional, default=20) <br> has_photos: boolean(optional)
DELETE /pets |`request body` <br> "ids": [list of ids]
###CLI
Выгрузка питомцев из командной строки в *stdout* в *JSON* формате

Необязательный параметр **has_photos: boolean**

`python <PROJECT_PATH>/manage.py get --has_photos=True`
### Развертывание с помощью docker
Для развертывания используйте команду: `docker-compose -f <PROJECT_PATH>/docker-compose.yml up`

### Запуск тестов
Для запуска тестов используйте команду: `python <PROJECT_PATH>/manage.py test`

### Переменные окружения
Для использования своих переменных окружений создайте файл `.env` в `<PROJECT_PATH>/pet/pet`