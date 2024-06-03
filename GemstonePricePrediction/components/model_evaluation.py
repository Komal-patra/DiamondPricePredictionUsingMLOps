import os
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
from GemstonePricePrediction.utils.utils import load_object

class ModelEvaluation:
    def __init__(self):
        pass
    
    @staticmethod
    def eval_metrics(actual, pred):
        """
        Evaluate the performance of the model using various metrics.
        """
        rmse = np.sqrt(mean_squared_error(actual, pred))  # RMSE
        mae = mean_absolute_error(actual, pred)  # MAE
        r2 = r2_score(actual, pred)  # R^2
        return rmse, mae, r2

    def initiate_model_evaluation(self, train_array, test_array):
        """
        Load the model, make predictions on the test set, and log the results to MLflow.
        """
        try:
            # Separate features and target from test array
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            # Load the pre-trained model
            model_path = os.path.join("artifacts", "model.pkl")
            model = load_object(model_path)

            # Set the MLflow tracking URI
            mlflow.set_tracking_uri('http://localhost:5000/')
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            # Start an MLflow run
            with mlflow.start_run():
                # Make predictions on the test set
                predicted_qualities = model.predict(X_test)

                # Evaluate the model
                rmse, mae, r2 = self.eval_metrics(y_test, predicted_qualities)

                # Log the metrics to MLflow
                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("mae", mae)
                mlflow.log_metric("r2", r2)

                # Log the model to MLflow
                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
                else:
                    mlflow.sklearn.log_model(model, "model")
        
        except Exception as e:
            raise e

