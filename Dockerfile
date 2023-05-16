FROM python:3.8

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY app/. .


RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libpq-dev \
    gcc \
    postgresql-client

RUN apt-get autoremove -y gcc

RUN chmod a+x /code/entrypoint.sh

ENTRYPOINT [ "/code/entrypoint.sh" ]
