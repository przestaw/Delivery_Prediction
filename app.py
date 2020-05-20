from sklearn.model_selection import train_test_split
import data_loader as data
import models_training as models


def train_models(x_train, x_test, y_train, y_test):
    model_xgb, params_xgb = models.train_model(y_train, x_train, model_type='xgb')
    print(params_xgb)

    model_tree, params_tree = models.train_model(y_train, x_train, model_type='tree')
    print(params_tree)

    model_knn, params_knn = models.train_model(y_train, x_train, model_type='knn')
    print(params_knn)

    models.compare_models([model_knn, model_tree, model_xgb], x_test, y_test)


if __name__ == "__main__":
    dataset = data.obtain_dataset_table()

    dataset, le_cat, le_subcat, le_city = data.code_labels(dataset)

    target = dataset['delivery_total_time_hours']
    data = dataset.drop(['delivery_total_time', 'delivery_total_time_hours'], axis=1)

    x_train, x_test, y_train, y_test = \
        train_test_split(data, target, test_size=0.2, random_state=0)

    train_models(x_train, x_test, y_train, y_test)
