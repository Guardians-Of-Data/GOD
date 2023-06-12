FROM python:3.9.0

WORKDIR /home/

RUN git clone https://github.com/Guardians-Of-Data/GOD.git

WORKDIR /home/GOD/

RUN pip install -r requirements.txt

RUN echo "SECRET_KEY=django-insecure-*_z0fq)g^w40yl5gojecey4$skx6a)p2giq_5$9b9gr)mkrmm9" > .env

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
