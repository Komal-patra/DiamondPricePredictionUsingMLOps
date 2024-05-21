from __future__ import annotations
import json
from textwrap import dedent
import pendulum
from airflow import DAG
from airflow import PythonOperator
from GemstonePricePrediction.pipelines.training_pipeline import TrainingPipeline

training_pipeline = TrainingPipeline()

with DAG(
    'gemstone_training_pipeline',
    default_args={'retries':2},
    description='My Gemstone Price prediction training pipeline',
    schedule_interval= '@weekly',
    start_date=pendulum.datetime(2024, 21, 5, tz="local"),
    catchup=False,
    tags=['machine_learning', 'classification','gemstone'],
) as dag:
    
    dag.doc_md = __doc__
    