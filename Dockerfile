FROM python:3.8-slim-buster
USER root

# Create and set working directory
RUN mkdir /app
WORKDIR /app

# Copy all files to the container
COPY . /app/

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Set environment variables
ENV AIRFLOW_HOME=/app/airflow
ENV AIRFLOW_CORE__DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW_CORE__ENABLE_XCOM_PICKLING=True

# Initialize the Airflow database
RUN airflow db init

# Create an Airflow user
RUN airflow users create \
    --username admin \
    --firstname komalfsds2022 \
    --lastname admin \
    --role Admin \
    --email komalfsds2022@gmail.com \
    --password admin

# Ensure the start.sh script is executable
RUN chmod +x /app/start.sh

# Update apt-get (optional, depending on your needs)
RUN apt-get update -y 

# Set entrypoint and command
ENTRYPOINT ["/bin/sh"]
CMD ["start.sh"]
