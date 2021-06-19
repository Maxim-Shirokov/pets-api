FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/rest_api_server

RUN pip install --upgrade pip

COPY requirements.txt /usr/src/rest_api_server
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/rest_api_server

COPY . .

RUN chmod a+x /usr/src/rest_api_server/entrypoint.sh

ENTRYPOINT ["/usr/src/rest_api_server/entrypoint.sh"]