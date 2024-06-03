from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import numpy as np
import pendulum

# Import custom components
from GemstonePricePrediction.components.data_ingestion import DataIngestion
from GemstonePricePrediction.components.data_transformation import DataTransformation
from GemstonePricePrediction.components.model_trainer import ModelTrainer
from GemstonePricePrediction.components.model_evaluation import ModelEvaluation
from GemstonePricePrediction.exception import CustomException
from GemstonePricePrediction.logger import logging
import sys

def start_data_ingestion():
    try:
        data_ingestion = DataIngestion()
        train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed successfully.")
        return {"train_data_path": train_data_path, "test_data_path": test_data_path}
    except Exception as e:
        logging.error("Error during data ingestion:", e)
        raise CustomException(e, sys)

def start_data_transformation(**kwargs):
    try:
        ti = kwargs['ti']
        paths = ti.xcom_pull(task_ids='data_ingestion')
        train_data_path = paths['train_data_path']
        test_data_path = paths['test_data_path']

        data_transformation = DataTransformation()
        train_arr, test_arr = data_transformation.initialize_data_transformation(train_data_path, test_data_path)
        logging.info("Data transformation completed successfully.")

        return {
            "train_arr": train_arr.tolist(),  # Convert numpy array to list
            "test_arr": test_arr.tolist()  # Convert numpy array to list
        }
    except Exception as e:
        logging.error("Error during data transformation:", e)
        raise CustomException(e, sys)

def start_model_training(**kwargs):
    try:
        ti = kwargs['ti']
        arrays = ti.xcom_pull(task_ids='data_transformation')
        train_arr = np.array(arrays['train_arr'])  # Convert list back to numpy array
        test_arr = np.array(arrays['test_arr'])  # Convert list back to numpy array

        model_trainer = ModelTrainer()
        model_trainer.initiate_model_training(train_arr, test_arr)
        logging.info("Model training completed successfully.")
    except Exception as e:
        logging.error("Error during model training:", e)
        raise CustomException(e, sys)



with DAG(
    "gemstone_training_pipeline",
    default_args={
        "owner": "airflow",
        "retries": 2,
        "retry_delay": timedelta(minutes=1),
        "start_date": datetime(2024, 1, 17, tzinfo=pendulum.timezone("UTC")),
        "email_on_failure": False,
        "email_on_retry": False,
    },
    description="Training pipeline for Gemstone Price Prediction",
    schedule_interval="@weekly",  # Weekly schedule
    catchup=False,
    tags=["machine_learning", "classification", "gemstone"],
) as dag:

    data_ingestion_task = PythonOperator(
        task_id='data_ingestion',
        python_callable=start_data_ingestion,
    )

    data_transformation_task = PythonOperator(
        task_id='data_transformation',
        python_callable=start_data_transformation,
        provide_context=True,
    )

    model_training_task = PythonOperator(
        task_id='model_training',
        python_callable=start_model_training,
        provide_context=True,
    )

    # Set task dependencies
    data_ingestion_task >> data_transformation_task >> model_training_task 
