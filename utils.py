import os
from pathlib import Path

def set_filename(filename):
    return filename

def load_environ():
    env_path = Path('.') / '.env'
    with open(env_path) as file:
        for line in file:
            key, value = line.strip().split('=')
            os.environ[key] = value