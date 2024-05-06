import os
import sys
import pandas as pd
from GemstonePricePrediction.exception import CustomException
from GemstonePricePrediction.logger import logging
from GemstonePricePrediction.utils.utils import load_object

class PredictPipeline:

    def __init__(self):
        print("init.. the object")

    def predict(self, features):
        try:
            preprocessor_path = os.path.join('artifacts','preprocessor.pkl')
            model_path = os.path.join('artifacts','model.pkl')

            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            scaled_fea = preprocessor.transform(features)
            prediction = model.predict(scaled_fea)

            return prediction

        except Exception as e:
            raise CustomException(e,sys)
        
class CustomData:

    def __init__(self):
        pass

    def get_data_as_dataframe(self):
        pass
