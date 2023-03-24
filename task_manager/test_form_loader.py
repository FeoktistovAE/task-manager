import json

from task_manager import FIXTURE_PATH


def load_form(form_name):
    with open(FIXTURE_PATH) as output:
        test_data = json.load(output)
    return test_data[form_name]
