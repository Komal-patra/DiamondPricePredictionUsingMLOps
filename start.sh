#!/bin/sh

# Start the Airflow web server and scheduler
airflow webserver --port 8080 & 
airflow scheduler
