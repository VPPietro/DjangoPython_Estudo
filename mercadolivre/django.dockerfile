FROM python:latest
LABEL Pietro Paraventi Vanelli
COPY . /usr/src/eshop
WORKDIR /usr/src/eshop


RUN source mlenv/bin/activate
# RUN adduser -D pietro
# USER pietro
# RUN pip install -r requirements.txt

# ENTRYPOINT python manage.py runserver 127.0.0.1:8000
EXPOSE 8000