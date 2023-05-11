FROM python:3.8

# port where the Django app runs  
EXPOSE 8000  
# setup environment variable  
ENV DockerHOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# where your code lives  
WORKDIR $DockerHOME  

COPY cesem/. $DockerHOME
# run this command to install all dependencies  
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libpq-dev \
    gcc \
    postgresql-client

RUN pip install psycopg2==2.8.3
RUN apt-get autoremove -y gcc

RUN chmod +x $DockerHOME/docker-entrypoint.sh

ENTRYPOINT [ "$DockerHOME/docker-entrypoint.sh" ]