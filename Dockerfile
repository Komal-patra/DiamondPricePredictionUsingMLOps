FROM python:3.8-slim-buster
USER root
RUN mkdir /app
COPY . /app/
WORKDIR /app/
RUN pip3 install -r requiremnts.txt
ENV AIRFLOW_HOME = '/app/airflow'
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT = 1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING = True
RUN airflow db init
RUN airflow users create -e komalfsds2022@gmail.com -f komalfsds2022 -p admin -r Admin -users
RUN chmod 777 start.sh
RUN apt update -y 
ENTRYPOINT [ "/bin/sh" ]
CMD [ "start.sh" ] 