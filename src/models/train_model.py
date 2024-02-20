import pathlib
import sys
import joblib
import mlflow
import pandas as pd
import numpy as np
from hyperopt import hp
from sklearn.model_selection import train_test_split
from hyperopt.pyll.base import scope
from sklearn.metrics import mean_squared_error
from hyperopt import hp, fmin, tpe, Trials, STATUS_OK, space_eval
from xgboost import XGBRegressor



def find_best_model_with_params(X_train, y_train, X_test, y_test):

    hyperparameters = {
        "RandomForestRegressor": {
            "n_estimators": hp.choice("n_estimators", [10, 15, 20]),
            "max_depth": hp.choice("max_depth", [6, 8, 10]),
            "max_features": hp.choice("max_features", ["sqrt", "log2", None]),
        },
        "XGBRegressor": {
            "n_estimators": hp.choice("n_estimators", [10, 15, 20]),
            "max_depth": hp.choice("max_depth", [6, 8, 10]),
            "learning_rate": hp.uniform("learning_rate", 0.03, 0.3),
        },
    }
    def evaluate_model(hyperopt_params):
        params = hyperopt_params
        if 'max_depth' in params: params['max_depth']=int(params['max_depth'])  
        if 'min_child_weight' in params: params['min_child_weight']=int(params['min_child_weight']) 
        if 'max_delta_step' in params: params['max_delta_step']=int(params['max_delta_step'])

        model = XGBRegressor(**params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        model_rmse = mean_squared_error(y_test, y_pred)
        mlflow.log_metric('RMSE', model_rmse) 
        loss = model_rmse  
        return {'loss': loss, 'status': STATUS_OK}
    space = hyperparameters['XGBRegressor']
    with mlflow.start_run(run_name='XGBRegressor'):
        argmin = fmin(
            fn=evaluate_model,
            space=space,
            algo=tpe.suggest,
            max_evals=5,
            trials=Trials(),
            verbose=True
            )
    run_ids = []
    with mlflow.start_run(run_name='XGB Final Model') as run:
        run_id = run.info.run_id
        run_name = run.data.tags['mlflow.runName']
        run_ids += [(run_name, run_id)]
        params = space_eval(space, argmin)
        if 'max_depth' in params: params['max_depth']=int(params['max_depth'])       
        if 'min_child_weight' in params: params['min_child_weight']=int(params['min_child_weight'])
        if 'max_delta_step' in params: params['max_delta_step']=int(params['max_delta_step'])  
        mlflow.log_params(params)

        model = XGBRegressor(**params)
        model.fit(X_train, y_train)
        mlflow.sklearn.log_model(model, 'model') 
    return model


def save_model(model, output_path):
    joblib.dump(model, output_path + "/model.joblib")


def main():
    curr_dir = pathlib.Path(__file__)
    home_dir = curr_dir.parent.parent.parent

    input_file = '/data/interim/'
    data_path = home_dir.as_posix() + input_file
    output_path = home_dir.as_posix() + "/models"
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)


    x_train=pd.read_csv(home_dir.as_posix()+'/data/processed/x_train.csv')
    x_test=pd.read_csv(home_dir.as_posix()+'/data/processed/x_test.csv')
    y_train=pd.read_csv(home_dir.as_posix()+'/data/processed/y_train.csv')
    y_test=pd.read_csv(home_dir.as_posix()+'/data/processed/y_test.csv')

    trained_model = find_best_model_with_params(x_train, y_train, x_test, y_test)
    save_model(trained_model, output_path)

if __name__=='__main__':
    main()
