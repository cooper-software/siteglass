import os.path

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def get(path):
    return os.path.join(DATA_DIR, path)