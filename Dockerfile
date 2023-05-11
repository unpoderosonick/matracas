# base image  
FROM python:3.8
# port where the Django app runs  
EXPOSE 8000  
# setup environment variable  
ENV DockerHOME=/app
# where your code lives  
WORKDIR $DockerHOME  

COPY cesem/. $DockerHOME
# run this command to install all dependencies  
RUN pip install -r requirements.txt


RUN python manage.py migrate


CMD ["manage.py", "runserver", "0.0.0.0:8000"]