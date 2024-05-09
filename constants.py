from pathlib import Path
import os
from utils import load_environ

load_environ()

# env_path = Path('.') / '.env'
# with open(env_path) as file:
#     for line in file:
#         key, value = line.strip().split('=')
#         os.environ[key] = value

FILE_NAME = os.getenv(key='FILE_NAME', default='data.json')
TEST_DATA_FILE_NAME = os.getenv(key='TEST_DATA_FILE_NAME', default='test_data.json')
# BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
# FILE_DIR = BASE_DIR / 'budget_files'
PRETTY_OUTPUT = 'pretty'
FILE_OUTPUT = 'file'
