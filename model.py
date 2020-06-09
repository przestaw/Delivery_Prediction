import numpy as np
import pandas as pd
from models_training import train_model
from data_loader import obtain_dataset_table, code_labels


class ModelHolder:
    def __init__(self):
        self.dataset = obtain_dataset_table()
        self.dataset, self.le_cat, self.le_subcat, self.le_city = code_labels(self.dataset)

        target = self.dataset['delivery_total_time_hours']
        data = self.dataset.drop(['delivery_total_time', 'delivery_total_time_hours'], axis=1)

        # TODO : export models and load from args here ??
        self.tree_model, _ = train_model(target, data, model_type='tree', randomized=True)
        self.xgb_model, _ = train_model(target, data, model_type='xgb', randomized=True)
        self.knn_model, _ = train_model(target, data, model_type='knn', randomized=True)

        self.history = []

    def make_prediction(self, company, city, price, category, subcategory, model='tree'):
        query = np.array([np.nan, np.nan, np.nan, np.nan, np.nan])

        query[0] = company
        query[1] = self.le_city.transform([city])[0]
        query[2] = price
        query[3] = self.le_cat.transform([category])[0]
        query[4] = self.le_subcat.transform([subcategory])[0]

        prediction = 0

        if model == 'tree':
            prediction = self.tree_model.predict(query.reshape(1, -1))[0]
        elif model == 'xgb':
            prediction = self.xgb_model.predict(query.reshape(1, -1))[0]
        elif model == 'knn':
            prediction = self.knn_model.predict(query.reshape(1, -1))[0]
        else:
            raise NotImplementedError

        # logging, history [data collection]
        self.history.append([company, city, price, category, subcategory, prediction, model])

        return prediction

    def get_predictions_history(self, flush=False):
        df = pd.DataFrame.from_records(self.history,
                                       columns=['delivery_company', 'city', 'price', 'category', 'subcategory',
                                                'prediction', 'model'])
        if flush:
            self.history = []

        return df

    def get_predictions_comparison(self, flush=False):
        df = self.get_predictions_history(flush)
        df = df.drop(axis='columns', labels=['prediction', 'model'])

        data = df.copy()
        data['city'] = self.le_city.transform(data['city'])
        data['category'] = self.le_cat.transform(data['category'])
        data['subcategory'] = self.le_subcat.transform(data['subcategory'])

        df['xgb_predictions'] = self.xgb_model.predict(data)
        df['tree_predictions'] = self.tree_model.predict(data)
        df['knn_predictions'] = self.knn_model.predict(data)
        df['actual'] = np.nan  # to be filled in next step when appropriate

        return df

    def update_model(self):
        # TODO - as needed
        raise NotImplementedError

    def configure_AB(self):
        # TODO - what could be configured
        raise NotImplementedError
