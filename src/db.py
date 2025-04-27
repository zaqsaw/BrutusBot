from tinydb import TinyDB, Query

def config():
    return TinyDB('config.json')

def set_token(token):
    config().insert({'key': 'TOKEN', 'value': token})

def get_token():
    return config().search(Query().key == "TOKEN")[0]['value']
