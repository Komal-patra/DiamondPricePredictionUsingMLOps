import os
import sys
import mlflow
import mlflow.sklearn
import numpy as np
import pickle
from GemstonePricePrediction.utils.utils import load_object
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from GemstonePricePrediction.logger import logging
from GemstonePricePrediction.exception import CustomException

class ModelEvaluation:

    def __init__(self):
        logging.info('Evaluation started')
    
    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))# here is RMSE
        mae = mean_absolute_error(actual, pred)# here is MAE
        r2 = r2_score(actual, pred)# here is r3 value
        logging.info("evaluation metrics captured")
        return rmse, mae, r2
    
    def initiate_model_evaluation(self, train_array, test_array):
        try:
            X_test, y_test = (test_array[:,:-1], test_array[:,-1])

            model_path = os.path.join('artifacts', 'model.pkl')
            model = load_object(model_path)

            logging.info('Model has register')

        except Exception as e:
            raise CustomException(e,sys)