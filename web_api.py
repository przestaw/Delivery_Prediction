from flask import Flask, jsonify, request, abort
import data_loader as data
import numpy as np

app = Flask(__name__)

dataset = data.obtain_dataset_table()
dataset, le_cat, le_subcat, le_city = data.code_labels(dataset)


@app.route('/', methods=['GET'])
@app.route('/name', methods=['GET'])
def name():
    return jsonify({
        'title': 'Projekt z Inzynierii Uczenia Maszynowego',
        'semester': '20L',
        'authors': ['Przemyslaw Stawczyk', 'Maciej Szulik'],
        'status': 'running'
    }), 200


@app.route('/api/v1.0/delivery_time/', methods=['GET'])
def delivery_time():
    if not request.json:
        abort(400)
    query = np.array([np.nan, np.nan, np.nan, np.nan, np.nan])

    # TODO : check, nan or error if missing
    query[0] = request.json['delivery_company']
    query[1] = le_city.transform(request.json['city'])
    query[2] = request.json['price']
    # optional?
    query[3] = le_cat.transform(request.json['category'])
    query[4] = le_subcat.transform(request.json['subcategory'])

    # TODO : modeling
    # prediction =  model.predict(query.reshape(1, -1))

    return jsonify({
        'prediction': 0.,
        'status': 'not yet implemented'
    }), 200


if __name__ == '__main__':
    app.run(debug=False)
