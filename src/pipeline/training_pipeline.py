import os
import sys
from src.logger.logging import logging
from src.exceptions.exceptions import customexception
import pandas as pd

from src.components.data_ingestion import DataIngestion


obj=DataIngestion()
train_data_path,test_data_path=obj.initiate_data_ingestion()