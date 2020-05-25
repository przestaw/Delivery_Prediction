import json
import numpy as np
import pandas as pd
from sklearn import preprocessing


def clean_nan_rows(dataframe, print_stats=False):
    clean_df = dataframe.dropna(axis=0, how='any')
    if print_stats:
        print('Original Length=', len(dataframe), '\tCleaned Length=', len(clean_df), '\tMissing Data=',
              len(dataframe) - len(clean_df))
    return clean_df


def load_file(filename):
    with open(filename, encoding="utf8") as f:
        data = f.readlines()
        data = [json.loads(line) for line in data]  # convert string to dict format
        df = pd.json_normalize(data)
    return df


def create_subcategories(products):
    category_path_arr = products['category_path'].str.split(';', 2)
    category_arr = []
    subcategory_arr = []
    for path in category_path_arr:
        if type(path) == float:
            category_arr.append(path)
            subcategory_arr.append(path)
        else:
            category_arr.append(path[0])
            subcategory_arr.append(path[1])

    products['category'] = category_arr
    products['subcategory'] = subcategory_arr

    return products


def fill_missing_user_id(sessions):
    session_user_map = sessions[sessions["user_id"].notna()].set_index('session_id')['user_id'].to_dict()

    for i, row in sessions.iterrows():
        if np.isnan(row["user_id"]) and row["session_id"] in session_user_map:
            sessions.at[i, 'user_id'] = session_user_map[row["session_id"]]

    buy_sessions = sessions[sessions.event_type == 'BUY_PRODUCT']

    clean_nan_rows(dataframe=buy_sessions['user_id'], print_stats=False)

    return buy_sessions


def load_tables():
    users = load_file(r'data/users.jsonl')
    deliveries = load_file("data/deliveries.jsonl")
    sessions = load_file("data/sessions.jsonl")
    products = load_file("data/products.jsonl")

    return users, deliveries, sessions, products


def obtain_dataset_table():
    users, deliveries, sessions, products = load_tables()

    # create subcategories and fill missing user id
    products = create_subcategories(products)
    sessions = fill_missing_user_id(sessions)

    # drop deliveries with missing delivery time
    deliveries = deliveries.dropna()

    # inner join sessions and deliveries
    merged_data = pd.merge(left=sessions, right=deliveries, left_on='purchase_id', right_on='purchase_id')

    # left join users
    merged_data = pd.merge(left=merged_data, right=users, how='left', left_on='user_id', right_on='user_id')

    # left join products
    merged_data = pd.merge(left=merged_data, right=products, how='left', left_on='product_id', right_on='product_id')

    # delivery time in hours
    merged_data['delivery_timestamp'] = \
        pd.to_datetime(merged_data.delivery_timestamp)
    merged_data['purchase_timestamp'] = \
        pd.to_datetime(merged_data.purchase_timestamp)
    merged_data['delivery_total_time'] = \
        merged_data['delivery_timestamp'] - merged_data['purchase_timestamp']

    merged_data['delivery_total_time_hours'] = \
        merged_data['delivery_total_time'].dt.total_seconds() / 3600

    # drop unnecessary columns
    columns = ['session_id', 'purchase_id', 'user_id', 'product_id', 'event_type',
               'offered_discount', 'name', 'timestamp', 'product_name', 'street',
               'purchase_timestamp', 'delivery_timestamp', 'category_path']
    for col in columns:
        merged_data = merged_data.drop(col, axis=1)

    merged_data = clean_nan_rows(merged_data, print_stats=False)

    return merged_data


def code_labels(dataset):
    # code labels
    le_cat = preprocessing.LabelEncoder()
    categories = np.unique(np.array(dataset['category']))
    np.append(categories, 'missing')
    le_cat.fit(categories)
    dataset['category'] = le_cat.transform(dataset['category'])

    le_subcat = preprocessing.LabelEncoder()
    subcategories = np.unique(np.array(dataset['subcategory']))
    np.append(subcategories, 'missing')
    le_subcat.fit(subcategories)
    dataset['subcategory'] = le_subcat.transform(dataset['subcategory'])

    le_city = preprocessing.LabelEncoder()
    cities = np.unique(np.array(dataset['city']))
    np.append(cities, 'missing')
    le_city.fit(cities)
    dataset['city'] = le_city.transform(dataset['city'])

    return dataset, le_cat, le_subcat, le_city
