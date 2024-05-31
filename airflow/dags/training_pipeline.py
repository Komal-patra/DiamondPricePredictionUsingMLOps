from __future__ import annotations
import json
from textwrap import dedent
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from GemstonePricePrediction.pipelines.training_pipeline import TrainingPipeline

training_pipeline = TrainingPipeline()

with DAG(
    'gemstone_training_pipeline',
    default_args={'retries': 2},
    description='My Gemstone Price prediction training pipeline',
    schedule_interval='@weekly',
    start_date=pendulum.datetime(2024, 5, 21, tz="local"),
    catchup=False,
    tags=['machine_learning', 'classification', 'gemstone'],
) as dag:
    
    dag.doc_md = __doc__

    def data_ingestion(**kwargs):
        ti = kwargs['ti']
        train_data_path, test_data_path = training_pipeline.start_data_ingestion()
        ti.xcom_push('data_ingestion_artifact', {'train_data_path': train_data_path, 'test_data_path': test_data_path})

    def data_transformations(**kwargs):
        ti = kwargs['ti']
        data_ingestion_artifact = ti.xcom_pull(task_ids='data_ingestion', key='data_ingestion_artifact')
        train_data_path = data_ingestion_artifact['train_data_path']
        test_data_path = data_ingestion_artifact['test_data_path']
        train_arr, test_arr = training_pipeline.start_data_transformation(train_data_path, test_data_path)
        train_arr = train_arr.tolist()
        test_arr = test_arr.tolist()
        ti.xcom_push('data_transformation_artifact', {'train_arr': train_arr, 'test_arr': test_arr})

    def model_trainer(**kwargs):
        import numpy as np
        ti = kwargs['ti']
        data_transformation_artifact = ti.xcom_pull(task_ids='data_transformations', key='data_transformation_artifact')
        train_arr = np.array(data_transformation_artifact['train_arr'])
        test_arr = np.array(data_transformation_artifact['test_arr'])
        training_pipeline.start_model_training(train_arr, test_arr)

    def push_data_to_s3(**kwargs):
        import os
        bucket_name = os.getenv('BUCKET_NAME')
        artifact_folder = '/app/artifacts'
        os.system(f'aws s3 sync {artifact_folder} s3://{bucket_name}/artifact')

    data_ingestion_task = PythonOperator(
        task_id='data_ingestion',
        python_callable=data_ingestion,
    )
    data_ingestion_task.doc_md = dedent(
        '''
        #### Data Ingestion Task   
        This task creates the train-test split.        
        '''
    )

    data_transform_task = PythonOperator(
        task_id='data_transformations',
        python_callable=data_transformations,
    )
    data_transform_task.doc_md = dedent(
        '''
        #### Data Transformation Task
        This task transforms the data into numpy arrays.
        '''
    )

    model_trainer_task = PythonOperator(
        task_id='model_trainer',
        python_callable=model_trainer,
    )
    model_trainer_task.doc_md = dedent(
        '''
        #### Model Trainer Task
        This task trains the model.
        '''
    )

    push_data_to_s3_task = PythonOperator(
        task_id='push_data_to_s3',
        python_callable=push_data_to_s3,
    )
    push_data_to_s3_task.doc_md = dedent(
        '''
        #### Push Data to S3 Task
        This task pushes the artifacts to S3.
        '''
    )

    data_ingestion_task >> data_transform_task >> model_trainer_task >> push_data_to_s3_task
