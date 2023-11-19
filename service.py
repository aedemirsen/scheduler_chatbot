import chat
import os
import json
import constants
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def response(question):
    res = chat.get_chatbot_response(question)
    return {"response": res}


def welcome():
    return {"response": constants.WELCOME_MESSAGE}


def get_api_key():
    return {"response": constants.GOOGLE_API_KEY}


def save_api_key(key):
    # save api key to db
    constants.GOOGLE_API_KEY = key
    return {"response": "Google Api Key Saved"}


def gpt_response(content):
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content}
        ],
        temperature=0,
        max_tokens=256
    )
    return res.choices[0].message.content


def extract_title(sentence):
    return gpt_response(constants.EXTRACT_TITLE.format(sentence))


def set_title(sentence):
    constants.NECESSARY_SCHEDULING_FORMAT['title'] = extract_title(sentence)
    print(constants.NECESSARY_SCHEDULING_FORMAT)
    return return_necessary_fields_info(constants.NECESSARY_SCHEDULING_FORMAT)


def format_schedule(schedule):
    formatted_string = (
        f"Hour: {schedule['hour']}\n"
        f"Minute: {schedule['minute']}\n"
        f"Title: {schedule['title']}\n"
        f"AM/PM: {schedule['am/pm']}\n"
        f"Day: {schedule['day']}\n"
        f"Month: {schedule['month']}\n"
        f"Year: {schedule['year']}"
    )
    return formatted_string


def return_necessary_fields_info(res):
    # create appropriate response
    # find undefined fields
    print(res)
    undefined_fields = find_empty_fields(res)
    print(undefined_fields)
    if 'month' in undefined_fields:
        res['month'] = 'current'
    if 'year' in undefined_fields:
        res['year'] = 'current'
    undefined_fields = find_empty_fields(res)
    print(undefined_fields)
    constants.NECESSARY_SCHEDULING_FORMAT = res
    if len(undefined_fields) == 0:
        # run google service to create event
        # send response whether successful or not
        print(constants.NECESSARY_SCHEDULING_FORMAT)
        success = True
        return constants.SUCCESSFULLY_CREATED if success else constants.FAIL_WHILE_CREATION

    print('XXXX')
    # ask user for undefined fields
    return constants.ASK_UNDEFINED_FIELDS + ', '.join(undefined_fields)


def ask_gpt_for_necessary_data(when):
    # gpt service
    res = gpt_response(constants.GPT_PROMPT_FOR_NECESSARY_FORMAT.format(when))
    res = str_to_json(res)
    res = merge_dictionaries(constants.NECESSARY_SCHEDULING_FORMAT, res)
    return return_necessary_fields_info(res)


def ask_gpt_for_tag(sentence):
    content = constants.GPT_PROMPT_FOR_TAG.format(sentence)
    return gpt_response(content)


def find_empty_fields(data, exclude_fields=None):
    """
    Takes a dictionary and returns a list of keys where the values are empty, excluding specified fields.

    :param data: Dictionary with potential empty values.
    :param exclude_fields: List of fields to exclude from the check.
    :return: List of keys with empty values, excluding the specified fields.
    """
    if exclude_fields is None:
        exclude_fields = []
    return [key for key, value in data.items() if not value and key not in exclude_fields]


def str_to_json(optional_str):
    """
    Convert an optional JSON-formatted string to a Python dictionary.

    :param optional_str: The string to convert.
    :return: A Python dictionary if the string is valid JSON, otherwise None.
    """
    if optional_str:
        try:
            return json.loads(optional_str)
        except json.JSONDecodeError:
            print("Error: String is not in valid JSON format.")
            return None
    else:
        print("No string provided.")
        return None


def merge_dictionaries(dict1, dict2):
    """
    Merge two dictionaries. Non-empty values from dict2 overwrite empty values in dict1.

    :param dict1: The first dictionary.
    :param dict2: The second dictionary.
    :return: Merged dictionary.
    """
    merged_dict = dict1.copy()  # Copy the first dictionary to avoid modifying the original
    for key in dict2:
        # Check if dict2 has a non-empty value and dict1 has an empty value for the same key
        if dict2[key] and not dict1[key]:
            merged_dict[key] = dict2[key]
    return merged_dict
