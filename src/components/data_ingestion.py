import os
import sys
import pandas as pd
import numpy as np
from src.logger.logging import logging
from src.exceptions.exceptions import customexception

from dataclasses import dataclass
from pathlib import Path
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    
    raw_data_path = os.path.join('artifacts','raw.csv')
    train_data_path = os.path.join('artifacts','train.csv')
    test_data_path = os.path.join('artifacts','test.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Data Ingestion started')
        try:
            data = pd.read_csv('C:/Komal_notes/ML_proj/DiamondPricePredictionUsingMLOps/data/DiamondGemstone.csv')
            logging.info('Reading a dataframe')

            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_data_path)),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info(' The raw data is saved in the artifact folder')

            logging.info('Further the data is splitted into train and test')

            train_data, test_data = train_test_split(data, test_size=0.25)
            logging.info('train-test split completed')

            train_data.to_csv(self.ingestion_config.train_data_path,index=False)
            test_data.to_csv(self.ingestion_config.test_data_path,index=False)

            logging.info('data ingestion completed')
            logging.info('==============================================')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.info()
            raise customexception(e,sys)
