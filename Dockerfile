FROM python: 3.9.0

WORKDIR /home/

RUN git clone https://github.com/hakjin34/encore.git

WORKDIR /home/GODproject/

RUN pip install -r requirements.txt