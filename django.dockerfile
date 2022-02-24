FROM python:latest
LABEL Pietro Paraventi Vanelli
COPY . /eshop
WORKDIR /eshop

# ENV VIRTUAL_ENV=/opt/mlenv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH ="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements2.txt

# ENTRYPOINT python manage.py runserver 127.0.0.1:8000
EXPOSE 8001