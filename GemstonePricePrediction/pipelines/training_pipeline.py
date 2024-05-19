import os
import sys

# Add the project root directory to the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from GemstonePricePrediction.logger import logging
from GemstonePricePrediction.exception import CustomException
import pandas as pd

from GemstonePricePrediction.components.data_ingestion import DataIngestion
from GemstonePricePrediction.components.data_transformation import DataTransformation
from GemstonePricePrediction.components.model_trainer import ModelTrainer
from GemstonePricePrediction.components.model_evaluation import ModelEvaluation

obj=DataIngestion()
train_data_path,test_data_path=obj.initiate_data_ingestion()

data_transformation=DataTransformation()
train_arr,test_arr=data_transformation.initialize_data_transformation(train_data_path,test_data_path)

model_trainer_obj=ModelTrainer()
model_trainer_obj.initate_model_training(train_arr,test_arr)

model_eval_obj = ModelEvaluation()
model_eval_obj.initiate_model_evaluation(train_arr,test_arr)