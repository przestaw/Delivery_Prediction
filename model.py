import numpy as np
import pandas as pd
from models_training import train_model
from data_loader import obtain_dataset_table, code_labels


class TreeModelHolder:
    def __init__(self):
        self.dataset = obtain_dataset_table()
        self.dataset, self.le_cat, self.le_subcat, self.le_city = code_labels(self.dataset)

        target = self.dataset['delivery_total_time_hours']
        data = self.dataset.drop(['delivery_total_time', 'delivery_total_time_hours'], axis=1)

        self.model, _ = train_model(target, data, model_type='tree', randomized=True)
        self.history = []

    def make_prediction(self, company, city, price, category, subcategory):
        query = np.array([np.nan, np.nan, np.nan, np.nan, np.nan])

        query[0] = company
        query[1] = self.le_city.transform([city])[0]
        query[2] = price
        query[3] = self.le_cat.transform([category])[0]
        query[4] = self.le_subcat.transform([subcategory])[0]

        prediction = self.model.predict(query.reshape(1, -1))[0]

        # logging, history [data collection]
        self.history.append([company, city, price, category, subcategory, prediction])
        # A/B experiment ??

        return prediction

    def get_predictions(self, flush=False):
        df = pd.DataFrame.from_records(self.history,
                                       columns=['delivery_company', 'city', 'price', 'category', 'subcategory',
                                                'tree_prediction'])
        if flush:
            self.history = []

        return df

    def update_model(self):
        # TODO
        raise NotImplementedError

    def configure_AB(self):
        # TODO
        raise NotImplementedError
