import pickle

def dump(model, model_name):
    with open("models/" + model_name, 'wb') as model_file:
        pickle.dump(model, model_file)  

def load(model_name):
    with open("models/"+model_name, 'rb') as model_file:
        model = pickle.load(model_file)
        return model
