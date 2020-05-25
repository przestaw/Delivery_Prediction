import json

from flask import Flask, jsonify, request, abort
import data_loader as data
import numpy as np
from models_training import train_model

app = Flask(__name__)

dataset = data.obtain_dataset_table()
dataset, le_cat, le_subcat, le_city = data.code_labels(dataset)

target = dataset['delivery_total_time_hours']
data = dataset.drop(['delivery_total_time', 'delivery_total_time_hours'], axis=1)

model, _ = train_model(target, data, model_type='tree', randomized=True)


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
    for it in ['delivery_company', 'city', 'price']:
        if 'delivery_company' not in request.json:
            missing_info.append(it)

    # error response if data is missing
    if len(missing_info) > 0:
        return jsonify({
            'status': 'missing information',
            'missing': str(missing_info)
        }), 418  # TODO remove joke

    # prepare query for model
    query = np.array([np.nan, np.nan, np.nan, np.nan, np.nan])

    query[0] = request.json['delivery_company']
    query[1] = le_city.transform([request.json['city']])[0]
    query[2] = request.json['price']

    # optional? FIXME
    if 'category' in request.json:
        query[3] = le_cat.transform([request.json['category']])[0]
    else:
        query[3] = le_cat.transform(['missing'])[0]

    if 'subcategory' in request.json:
        query[4] = le_subcat.transform([request.json['subcategory']])[0]
    else:
        query[4] = le_subcat.transform(['missing'])[0]

    prediction = model.predict(query.reshape(1, -1))

    return jsonify({
        'prediction': prediction[0],
        'status': 'running'
    }), 200


if __name__ == '__main__':
    app.run(debug=False)
