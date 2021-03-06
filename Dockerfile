#-----------------------------------------------
# Dockerfile to build Docker Image of forum
#-----------------------------------------------

FROM python:3

WORKDIR /code
COPY ./forum /code
COPY requirements.txt /code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python manage.py collectstatic --noinput
CMD python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000
EXPOSE 8000
