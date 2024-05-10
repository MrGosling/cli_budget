import os
from utils import load_environ

load_environ()

FILE_NAME = os.getenv(key='FILE_NAME', default='data.json')
