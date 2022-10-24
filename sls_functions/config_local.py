import os
import sys

BASE_PATH = os.getcwd()

sys.path.append(f"{BASE_PATH}/layers/backend/python")
sys.path.append(f"{BASE_PATH}/../layers/django_requirements/python")
sys.path.append(f"{BASE_PATH}/../layers/boto_requirements/python")
