FROM python:2.7-stretch
MAINTAINER Patryk Galczynski <galczynski.patryk@gmail.com>
RUN apt-get update
RUN apt-get install -y git less vim cron unzip wget
RUN git clone https://github.com/evemorgen/nvdapi.git /root/nvdapi/
COPY db.sqlite3 /root/nvdapi/db.sqlite3
COPY cronjob /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN chmod 0644 /root/nvdapi/cron.py
RUN touch /var/log/cron.log
WORKDIR /root/nvdapi/
RUN pip install -r requirements.txt
RUN echo 'SECRET_KEY = "whatever"' >> nvdapi/local_settings.py
EXPOSE 1911
CMD service cron start && cd /root/nvdapi/ && python manage.py runserver 0.0.0.0:1911
