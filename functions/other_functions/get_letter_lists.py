import json

def get_lower_case() -> tuple:
    with open('./json_data/letters/lower_case_letters.json', 'r') as file:
        lower_case_letters = json.load(file)['lower_case_letters']
        file.close()

    return lower_case_letters

def get_upper_case() -> tuple:
    with open('./json_data/letters/upper_case_letters.json', 'r') as file:
        upper_case_letters = json.load(file)['upper_case_letters']
        file.close()

    return upper_case_letters