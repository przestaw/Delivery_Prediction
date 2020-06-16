from flask import Flask, jsonify, request, abort
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from data_loader import obtain_dataset_table, code_labels
from model import ModelHolder

app = Flask(__name__)

model = None


@app.route('/', methods=['GET'])
@app.route('/name', methods=['GET'])
def name():
    return jsonify({
        'title': 'Projekt z Inzynierii Uczenia Maszynowego',
        'semester': '20L',
        'authors': ['Przemyslaw Stawczyk', 'Maciej Szulik'],
        'status': 'running'
    }), 200


@app.route('/api', methods=['GET'])
def delivery_time():
    if not request.json:
        abort(400)

    missing_info = []
    for it in ['delivery_company', 'city', 'price', 'category', 'subcategory']:
        if it not in request.json:
            missing_info.append(it)

    # error response if data is missing
    if len(missing_info) > 0:
        return jsonify({
            'status': 'missing information',
            'missing': str(missing_info)
        }), 418  # TODO remove joke

    # prepare query for model

    company = int(request.json['delivery_company'])
    city = request.json['city']
    price = float(request.json['price'])

    category = request.json['category']
    subcategory = request.json['subcategory']

    prediction = model.make_prediction(company, city, price, category, subcategory)

    return jsonify({
        'prediction': prediction,
        'status': 'running'
    }), 200


@app.route('/api/history', methods=['GET'])
def delivery_time_history():
    history = model.get_predictions_history()

    return history.to_json(orient='records'), 200


@app.route('/api/summary', methods=['GET'])
def delivery_time_summary():
    history = model.get_predictions_comparison()

    return history.to_json(orient='records'), 200


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

    # xgb_model = XGBRegressor()
    # xgb_model.set_params(params={'eval_metric': 'rmse',
    #                              'learning_rate': 0.05,
    #                              'max_depth': 5,
    #                              'min_child_weight': 7,
    #                              'n_estimators': 100,
    #                              'objective': 'reg:squarederror',
    #                              'seed': 42,
    #                              'silent': 1})
    # xgb_model.fit(X=data, y=target)
    # FIXME : watafak xgboost
    #         ValueError: feature_names mismatch: ['delivery_company', 'city', 'price', 'category', 'subcategory'] ['f0', 'f1', 'f2', 'f3', 'f4']
    #         expected city, price, category, subcategory, delivery_company in input data

    models = [{'name': 'tree model', 'model': tree_model},
              # {'name': 'xgb model', 'model': xgb_model},
              {'name': 'knn model', 'model': knn_model}]
    model = ModelHolder(models, le_cat, le_subcat, le_city)
    model.configure_ab(True, 0)

    app.run(debug=False)
