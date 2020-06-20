
from data_loader import obtain_dataset_table, code_labels
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from model_files_manager import dump

if __name__ == '__main__':
    dataset = obtain_dataset_table()
    dataset, le_cat, le_subcat, le_city = code_labels(dataset)

    target = dataset['delivery_total_time_hours']
    data = dataset.drop(['delivery_total_time', 'delivery_total_time_hours'], axis=1)
    data = data[['delivery_company', 'city', 'price', 'category', 'subcategory']]

    ## TODO : export models and load from args here ??
    # tree_model, _ = train_model(target, data, model_type='tree', randomized=True)
    # xgb_model, _ = train_model(target, data, model_type='xgb', randomized=True)
    # knn_model, _ = train_model(target, data, model_type='knn', randomized=True)

    tree_model = DecisionTreeRegressor(criterion='friedman_mse',
                                       max_depth=7,
                                       min_samples_leaf=4,
                                       min_samples_split=2,
                                       random_state=42,
                                       splitter='random')
    tree_model.fit(X=data, y=target)

    knn_model = KNeighborsRegressor(algorithm='ball_tree',
                                    n_neighbors=26,
                                    weights='distance')
    knn_model.fit(X=data, y=target)

    xgb_model = XGBRegressor()
    xgb_model.set_params(params={'eval_metric': 'rmse',
                                 'learning_rate': 0.05,
                                 'max_depth': 5,
                                 'min_child_weight': 7,
                                 'n_estimators': 100,
                                 'objective': 'reg:squarederror',
                                 'seed': 42,
                                 'silent': 1})
    xgb_model.fit(X=data, y=target)
    # : "ME : watafak xgboost
    #         ValueError: feature_names mismatch: ['delivery_company', 'city', 'price', 'category', 'subcategory'] ['f0', 'f1', 'f2', 'f3', 'f4']
    #         expected city, price, category, subcategory, delivery_company in input data

    dump(tree_model, "tree_model.pkl")
    dump(knn_model, "knn_model.pkl")
    dump(xgb_model, "xgb_model.pkl")
  