from flask import Flask, jsonify, request, abort
from model import ModelHolder

app = Flask(__name__)

model = ModelHolder()


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

    # optional? FIXME -> if not add to missing info loop
    category, subcategory = None, None
    if 'category' in request.json:
        category = request.json['category']
    else:
        category = 'missing'

    if 'subcategory' in request.json:
        subcategory = request.json['subcategory']
    else:
        subcategory = 'missing'

    # TODO : A/B experiment -> if configured
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
    app.run(debug=False)
