from flask import Flask, jsonify, request, abort
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from data_loader import obtain_dataset_table, code_labels
from model_holder import ModelHolder
from model_files_manager import load
import json

app = Flask(__name__)

model_holder = None


@app.route('/', methods=['GET'])
@app.route('/api/info', methods=['GET'])
def name():
    return jsonify({
        'title': 'Projekt z Inzynierii Uczenia Maszynowego',
        'semester': '20L',
        'authors': ['Przemyslaw Stawczyk', 'Maciej Szulik'],
        'status': 'running'
    }), 200


@app.route('/api/prediction', methods=['GET'])
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
        }), 400

    # prepare query for model

    company = int(request.json['delivery_company'])
    city = request.json['city']
    price = float(request.json['price'])

    category = request.json['category']
    subcategory = request.json['subcategory']

    prediction = model_holder.make_prediction(company, city, price, category, subcategory)

    return jsonify({
        'prediction': prediction,
        'status': 'running'
    }), 200



@app.route('/api/prediction/history', methods=['GET'])
def delivery_time_history():
    history = model_holder.get_predictions_history()

    return history.to_json(orient='records'), 200


@app.route('/api/prediction/summary', methods=['GET'])
def delivery_time_summary():
    history = model_holder.get_predictions_comparison()

    return history.to_json(orient='records'), 200

@app.route('/api/prediction/models', methods=['GET'])
def get_models():
    models = model_holder.models
    output = [{'name': model['name'], 'filename': model['filename']} for model in models]

    return json.dumps(output), 200


@app.route('/api/prediction/models', methods=['POST'])
def add_model():
    if not request.json:
        abort(400)

    missing_info = []
    for it in ['name', 'filename']:
        if it not in request.json:
            missing_info.append(it)

    # error response if data is missing
    if len(missing_info) > 0:
        return jsonify({
            'status': 'missing information',
            'missing': str(missing_info)
        }), 400  
    
    for model in model_holder.models:
        if request.json['name'] == model['name']:
            model['model'] = load(request.json['filename']),
            model['filename'] = request.json['filename']
            return jsonify({
                'status': 'model replaced',
                }), 200

    model_holder.models.append({
        'name': request.json['name'],
        'model': load(request.json['filename']),
        'filename': request.json['filename']
    })

    return jsonify({'status': 'model added'}), 200



@app.route('/api/prediction/models/active', methods=['GET'])
def get_active_model():
    model = model_holder.models[model_holder.def_mod]
    output = {'name': model['name'], 'filename': model['filename']}

    return json.dumps(output), 200

@app.route('/api/prediction/models/active', methods=['POST'])
def set_active_model():
    if not request.json:
        abort(400)
    missing_info = []
    for it in ['name']:
        if it not in request.json:
            missing_info.append(it)

    # error response if data is missing
    if len(missing_info) > 0:
        return jsonify({
            'status': 'missing information',
            'missing': str(missing_info)
        }), 400
    
    errors = []
    if not model_holder.set_default_model(request.json['name']):
        errors.append("cannot set model B, model with given name does not exist")
    # error response if data is missing
    if len(errors) > 0:
        return jsonify({
            'status': 'missing model(s)',
            'missing': str(errors)
        }), 400    
    
    return jsonify({'status': 'model changed'}), 200   


@app.route('/api/prediction/AB', methods=['GET'])
def get_AB_status():
    return jsonify({'status': 'ok', 'active': model_holder.ab}), 200

@app.route('/api/prediction/AB', methods=['POST'])
def set_AB_status():
    if not request.json:
        abort(400)
    missing_info = []
    for it in ['active']:
        if it not in request.json:
            missing_info.append(it)

    # error response if data is missing
    if len(missing_info) > 0:
        return jsonify({
            'status': 'missing information',
            'missing': str(missing_info)
        }), 400  
    
    model_holder.ab = bool(request.json["active"])
    return jsonify({'status': 'ok', 'active': model_holder.ab}), 200   

@app.route('/api/prediction/AB/models', methods=['GET'])
def get_AB_models():
    return jsonify({'status': 'ok', 'models':
    {
        'A': model_holder.models[model_holder.new_mod]['name'],
        'B': model_holder.models[model_holder.def_mod]['name']
    }}), 200

@app.route('/api/prediction/AB/models', methods=['POST'])
def set_AB_models():
    if not request.json:
        abort(400)
    missing_info = []
    for it in ['A', 'B']:
        if it not in request.json:
            missing_info.append(it)

    # error response if data is missing
    if len(missing_info) > 0:
        return jsonify({
            'status': 'missing information',
            'missing': str(missing_info)
        }), 400
    
    errors = []
    if not model_holder.set_new_model(request.json['A']):
        errors.append("cannot set model A, model with given name does not exist")
    if not model_holder.set_default_model(request.json['B']):
        errors.append("cannot set model B, model with given name does not exist")
    # error response if data is missing
    if len(errors) > 0:
        return jsonify({
            'status': 'missing model(s)',
            'missing': str(errors)
        }), 400    
    
    return jsonify({'status': 'ok', 'active': model_holder.ab}), 200   

if __name__ == '__main__':
    dataset = obtain_dataset_table()
    dataset, le_cat, le_subcat, le_city = code_labels(dataset)

    # models = [
    # {'name': 'tree model', 'model': load("tree_model.pkl"), 'filename': "tree_model.pkl"},
    # {'name': 'knn model', 'model': load("knn_model.pkl"), 'filename': "knn_model.pkl"},
    # {'name': 'xgb model','model': load("xgb_model.pkl"), 'filename': "xgb_model.pkl"}]
    model_holder = ModelHolder([], le_cat, le_subcat, le_city)

    app.run(debug=False)
