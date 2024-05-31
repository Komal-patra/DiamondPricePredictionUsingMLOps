FROM python:3.8-slim-buster
USER root
# Create and set the working directory
RUN mkdir /app
COPY . /app/
WORKDIR /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/app/airflow
ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True

# Initialize the Airflow database and create the admin user
RUN airflow db init
RUN airflow users create -u admin -p admin -f Admin -l Admin -r Admin -e admin@example.com

# Make sure your start.sh script is executable
RUN chmod +x start.sh

# Set the entry point to start Airflow
ENTRYPOINT ["/bin/sh"]
CMD ["start.sh"]
