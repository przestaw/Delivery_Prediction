import json

from flask import Flask, jsonify, request, abort
import numpy as np

from model import TreeModelHolder

app = Flask(__name__)

model = TreeModelHolder()


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

    company = request.json['delivery_company']
    city = request.json['city']
    price = request.json['price']

    # optional? FIXME
    category, subcategory = None, None
    if 'category' in request.json:
        category = request.json['category']
    else:
        category = 'missing'

    if 'subcategory' in request.json:
        subcategory = request.json['subcategory']
    else:
        subcategory = 'missing'

    prediction = model.make_prediction(company, city, price, category, subcategory)

    return jsonify({
        'prediction': prediction,
        'status': 'running'
    }), 200


@app.route('/api/history', methods=['GET'])
def delivery_time_history():
    history = model.get_predictions()

    return history.to_json(orient='records'), 200


if __name__ == '__main__':
    app.run(debug=False)
