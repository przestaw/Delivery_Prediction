
from data_loader import obtain_dataset_table, code_labels
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from model_files_manager import dump
from models_training import train_model

if __name__ == '__main__':
    dataset = obtain_dataset_table()
    dataset, le_cat, le_subcat, le_city = code_labels(dataset)

    target = dataset['delivery_total_time_hours']
    data = dataset.drop(['delivery_total_time', 'delivery_total_time_hours'], axis=1)
    data = data[['delivery_company', 'city', 'price', 'category', 'subcategory']]

    tree_model, tree_hyperparameters = train_model(target, data, model_type='tree', randomized=True)
    xgb_model, xgb_hyperparameters = train_model(target, data, model_type='xgb', randomized=True)
    knn_model, knn_hyperparameters = train_model(target, data, model_type='knn', randomized=True)

    dump(tree_model, "tree_model.pkl")
    dump(knn_model, "knn_model.pkl")
    dump(xgb_model, "xgb_model.pkl")
  