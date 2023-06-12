FROM python:3.9.0

WORKDIR /home/

RUN echo "testing1234"

RUN git clone https://github.com/Guardians-Of-Data/GOD.git

WORKDIR /home/GOD/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

RUN echo "SECRET_KEY=django-insecure-*_z0fq)g^w40yl5gojecey4$skx6a)p2giq_5$9b9gr)mkrmm9" > .env

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate --settings=GODproject.settings.deploy && gunicorn GODproject.wsgi --env DJANGO_SETTINGS_MODULE=GODproject.settings.deploy --bind 0.0.0.0:8000"]

