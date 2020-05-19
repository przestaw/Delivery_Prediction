from flask import Flask, jsonify
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


@app.route('/delivery_time', methods=['GET'])
def delivery_time():
    query = np.array([np.nan, np.nan, np.nan, np.nan, np.nan])

    return jsonify({

        'status': 'not yet implemented'
    }), 200


if __name__ == '__main__':
    app.run(debug=False)
