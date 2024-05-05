import os
import sys
from GemstonePricePrediction.logger import logging
from GemstonePricePrediction.exception import CustomException
import pandas as pd

from GemstonePricePrediction.components.data_ingestion import DataIngestion



obj=DataIngestion()

train_data_path,test_data_path=obj.initiate_data_ingestion()
