import pandas as pd
import xgboost as xgb
from sklearn.metrics import max_error, mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, KFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor


def train_model(target, data, model_type='xgb', random_seed=42, randomized=True):
    params = {}
    model = None
    crv = None
    n_iter = 0

    if model_type == 'xgb':
        model = xgb.XGBRegressor()
        params = {
            'objective': ['reg:squarederror'],
            'eval_metric': ['rmse'],
            'learning_rate': [0.03, 0.05, 0.07],  # so called `eta` value
            'max_depth': [4, 5, 6, 7],
            'min_child_weight': [4],
            'silent': [1],
            'n_estimators': [200, 320, 450, 600],
            'seed': [random_seed]
        }
        n_iter = 28
    elif model_type == 'tree':
        model = DecisionTreeRegressor()
        params = {
            'max_depth': [3, 4, 5, 6, 7, 8, 9],
            'random_state': [random_seed],
            'criterion': ['mse', 'friedman_mse', 'mae'],
            'splitter': ['best', 'random']
        }
        n_iter = 22  # ~half of possible combinations
    elif model_type == 'knn':
        model = KNeighborsRegressor()
        params = {
            'n_neighbors': [3, 4, 5, 6, 8, 12, 15, 18, 22],
            'weights': ['uniform', 'distance'],
            'algorithm': ['ball_tree', 'kd_tree'],
        }
        n_iter = 20  # ~half of possible combinations
    else:
        return NotImplemented

    if randomized:
        crv = RandomizedSearchCV(model, params, random_state=random_seed, n_iter=n_iter,
                                 cv=KFold(n_splits=4, random_state=random_seed, shuffle=True), refit=True,
                                 scoring='neg_mean_squared_error')
    else:
        crv = GridSearchCV(model, params, cv=KFold(n_splits=4, random_state=random_seed, shuffle=True), refit=True,
                           scoring='neg_mean_squared_error')

    crv.fit(data, target)

    return crv.best_estimator_, crv.best_params_


def calc_metrics(predictions, test_y):
    err = max_error(test_y, predictions)
    avg = mean_absolute_error(test_y, predictions)
    avg_sqr = mean_squared_error(test_y, predictions)

    return [err, avg, avg_sqr]


def compare_models(models, test_X, test_y):
    test_predictions = []
    for mdl in models:
        test_predictions.append(mdl.predict(test_X))

    err = []
    for mdl_pred in test_predictions:
        err.append(calc_metrics(mdl_pred, test_y))

    error = pd.DataFrame.from_records(err, columns=['max error', 'avg error', 'avg sqr error'],
                                      index=['mdl-' + str(index + 1) for index in range(len(models))])
    ret = pd.DataFrame.from_records(test_X)
    ret['target'] = test_y
    for index, mdl in enumerate(models):
        ret['mdl-' + str(index + 1)] = test_predictions[index]

    return ret, error
