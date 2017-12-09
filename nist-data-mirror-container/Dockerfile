FROM openjdk:7
RUN apt-get update && apt-get -y install cron sqlite3
ADD crontab /etc/cron.d/basic-cron
RUN chmod 0644 /etc/cron.d/basic-cron
RUN touch /var/log/cron.log
RUN mkdir -p /root/nist-mirror-app/ /root/nist-mirror-data/
COPY nist-data-mirror.jar /root/nist-mirror-app/nist-data-mirror.jar
#CMD ["java", "-jar", "nist-data-mirror.jar", "/root/nist-mirror-data/"]
#CMD cron && tail -f /var/log/cron.log
CMD ["cron", "-f"]

